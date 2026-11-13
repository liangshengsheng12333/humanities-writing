"""Conservative text-review hints; never certifies evidence or rewrites text.

Examples:
    python review.py essay.md --mode general
    python review.py paper.md --mode academic --unit document --require 摘要
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys


@dataclass
class Issue:
    rule: str
    line: int
    message: str
    context: str = ""
    severity: str = "info"


def _editable_lines(text: str):
    """Exclude fenced code and block quotes; keep line numbers stable."""
    fence = None
    for number, raw in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", raw)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            yield number, ""
            continue
        if fence or raw.lstrip().startswith(">"):
            yield number, ""
            continue
        yield number, raw


def _mask_quotes(text: str) -> str:
    """Track nested quotes across lines; retain newlines and source line numbers."""
    pairs = {"“": "”", "‘": "’", "「": "」", "『": "』", '"': '"', "'": "'"}
    stack = []
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        if char == "`" and not stack:
            run = re.match(r"`+", text[i:]).group()
            end = text.find(run, i + len(run))
            if end >= 0:
                result.extend("\n" if c == "\n" else " " for c in text[i:end + len(run)])
                i = end + len(run)
                continue
        escaped = False
        previous = i - 1
        while previous >= 0 and text[previous] == "\\":
            escaped = not escaped
            previous -= 1
        apostrophe = (char == "'" and i > 0 and i + 1 < len(text)
                      and text[i - 1].isalnum() and text[i + 1].isalnum())
        protected = bool(stack)
        if stack and char == stack[-1] and not escaped:
            stack.pop()
        elif char in pairs and not escaped and not apostrophe:
            if not stack or stack[-1] not in {'"', "'"}:
                stack.append(pairs[char])
            protected = True
        result.append("\n" if char == "\n" else " " if protected else char)
        i += 1
    return "".join(result)


def _heading_name(raw: str) -> str:
    """Recognize standalone headings, numbered variants and title-colon forms."""
    title = raw.strip()
    title = re.sub(r"^#{1,6}\s*", "", title)
    title = title.strip("*").strip()
    title = re.sub(r"^(?:第[零〇一二三四五六七八九十百\d]+[章节]\s*|"
                   r"[（(][零〇一二三四五六七八九十百\d]+[）)]\s*|"
                   r"[零〇一二三四五六七八九十百\d]+(?:\.\d+)*[、.．：:]?\s+|"
                   r"[零〇一二三四五六七八九十百\d]+[、.．：:])", "", title)
    title = re.split(r"[:：]", title, maxsplit=1)[0].strip().strip("*").strip()
    return re.sub(r"\s+", "", title)


def review(text: str, mode: str = "academic", unit: str = "fragment",
           required: tuple[str, ...] = (), current_year: int | None = None) -> list[Issue]:
    if mode not in {"academic", "general"} or unit not in {"fragment", "document"}:
        raise ValueError("Invalid mode or unit")
    year = current_year if current_year is not None else datetime.now(
        timezone(timedelta(hours=8))).year
    issues = []
    editable = list(_editable_lines(text))
    masked = _mask_quotes("\n".join(raw for _, raw in editable)).split("\n")
    for (number, raw), visible in zip(editable, masked):
        if not raw:
            continue
        context = raw.strip()[:100]
        if re.search(r"\[(?:待补充|待查证)[^\]]*\]", visible):
            issues.append(Issue("EVIDENCE-TODO", number, "定稿前处理证据或出处缺口", context))
        if re.search(r"(?:有学者|一些学者|专家|研究|数据)(?:指出|认为|表明|显示)", visible):
            issues.append(Issue("SOURCE-CHECK", number,
                                "核对是否已有对应作者、来源或注释；不要仅凭措辞判错", context))
        for match in re.finditer(r"[（(]\s*((?:19|20)\d{2})\s*[)）]", visible):
            if int(match.group(1)) > year:
                issues.append(Issue("YEAR-CHECK", number,
                                    "文献年份晚于当前年份；核查待刊信息，不直接判为虚构", context))
        if re.search(r"^[①②③④⑤⑥⑦⑧⑨⑩]\s*$", visible.strip()):
            issues.append(Issue("EMPTY-NOTE", number, "注释编号后没有内容", context, "warning"))
        if re.search(r"意义重大|赋能|谱写新的篇章|未来可期|至关重要", visible):
            issues.append(Issue("STYLE-CHECK", number,
                                "检查评价是否有具体对象与证据；合理用法可以保留", context))
        if mode == "general" and re.search(r"希望这对你有帮助|下面是为你整理的|如有需要请", visible):
            issues.append(Issue("CHAT-CHECK", number,
                                "检查此处是否为作品正文中的聊天残留", context))
    if unit == "document":
        headings = {_heading_name(line) for line in masked if line.strip()}
        for section in required:
            if re.sub(r"\s+", "", section) not in headings:
                issues.append(Issue("REQUIRED-SECTION", 0,
                                    f"未识别到指定标题“{section}”；检查实际版式或标题写法"))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="按模式和文本范围输出审校提示，不自动修改")
    parser.add_argument("input", help="UTF-8 file, or - for stdin")
    parser.add_argument("--mode", choices=["academic", "general"], default="academic")
    parser.add_argument("--unit", choices=["fragment", "document"], default="fragment")
    parser.add_argument("--require", action="append", default=[], help="Explicit required section title")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--year", type=int, help="Override reference year")
    args = parser.parse_args()
    text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8-sig")
    issues = review(text, args.mode, args.unit, tuple(args.require), args.year)
    result = {"mode": args.mode, "unit": args.unit,
              "notice": "仅为候选提示；未核实事实、文献、引文或论证，不自动改稿",
              "total": len(issues), "issues": [asdict(issue) for issue in issues]}
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["notice"])
        if not issues:
            print("未发现此工具可识别的提示项。")
        for issue in issues:
            print(f"[{issue.rule}] line {issue.line}: {issue.message}")
            if issue.context:
                print(f"  {issue.context}")


if __name__ == "__main__":
    main()
