"""引文自动生成

根据已知元数据生成 GB/T 7714、Chicago、MLA 风格的简化引文草稿。
不保证完整规范；未知文献类型保持未知，不从期刊字段缺失推断专著。

注意：自动生成的引文可能因元数据不完整而需要人工校对。
建议在论文定稿时逐条核对。
"""
from __future__ import annotations

from .schema import Paper


def _join_authors_gbt(authors: list[str], max_show: int = 3) -> str:
    """GB/T 7714 作者格式：最多3人，超出用'等'"""
    if not authors:
        return ""
    shown = authors[:max_show]
    result = ", ".join(shown)
    if len(authors) > max_show:
        result += ", 等"
    return result


def _join_authors_chicago(authors: list[str], max_show: int = 3) -> str:
    """保留原姓名顺序，按Chicago风格连接作者"""
    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    shown = authors[:max_show]
    if len(authors) > max_show:
        return ", ".join(shown) + ", et al."
    return ", ".join(shown[:-1]) + f", and {shown[-1]}"


def _join_authors_mla(authors: list[str]) -> str:
    """保留原姓名顺序，按MLA风格连接作者"""
    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]}, and {authors[1]}"
    if len(authors) >= 3:
        return f"{authors[0]}, et al."
    return authors[0]


def gbt7714(paper: Paper, doc_type: str = "") -> str:
    """生成GB/T 7714风格的简化草稿；显式doc_type优先，未知类型需核对。"""
    parts: list[str] = []

    # 作者
    author_str = _join_authors_gbt(paper.authors)
    if author_str:
        parts.append(author_str)

    # 标题 + 文献类型标识
    if paper.title:
        parts.append(f"{paper.title}[{doc_type or paper.document_type or '类型待核对'}]")

    # 期刊/出版信息
    if paper.venue:
        parts.append(paper.venue)

    # 年份
    if paper.year:
        parts.append(str(paper.year))

    # DOI（如果有）
    if paper.doi:
        parts.append(f"DOI: {paper.doi}")

    return ". ".join(parts) + "."


def chicago_note(paper: Paper) -> str:
    """生成Chicago风格的简化草稿，出版项与页码仍需核对。"""
    parts: list[str] = []

    # 作者
    author_str = _join_authors_chicago(paper.authors)
    if author_str:
        parts.append(author_str)

    # 标题（期刊文章用引号，书用斜体标记）
    if paper.title:
        if paper.document_type in {"J", "C"}:
            parts.append(f'"{paper.title}"')
        else:
            parts.append(paper.title)  # 类型未知时不猜测；专著排版另行核对

    # 期刊名和年份
    if paper.venue and paper.year:
        parts.append(f"{paper.venue} ({paper.year})")
    elif paper.venue:
        parts.append(paper.venue)
    elif paper.year:
        parts.append(f"({paper.year})")

    return ", ".join(parts) + "."


def mla(paper: Paper) -> str:
    """生成MLA风格的简化草稿，不执行姓名倒置或补充缺失出版项。"""
    parts: list[str] = []

    # 作者
    author_str = _join_authors_mla(paper.authors)
    if author_str:
        parts.append(author_str)

    # 标题
    if paper.title:
        if paper.document_type in {"J", "C"}:
            parts.append(f'"{paper.title}."')
        else:
            parts.append(f"{paper.title}.")  # 未知类型保持原题名

    # 期刊/出版信息
    if paper.venue:
        venue_part = paper.venue
        if paper.year:
            venue_part += f", {paper.year}"
        parts.append(venue_part)
    elif paper.year:
        parts.append(str(paper.year))

    return " ".join(parts).rstrip(".") + "."


def auto_cite(paper: Paper, style: str = "gbt7714") -> str:
    """根据指定样式生成简化引文草稿

    Args:
        paper: 论文对象
        style: 引用样式，可选 'gbt7714' / 'chicago' / 'mla'

    Returns:
        待核对的引文草稿字符串
    """
    formatters = {
        "gbt7714": gbt7714,
        "chicago": chicago_note,
        "mla": mla,
    }

    if style.lower() not in formatters:
        raise ValueError("Unknown citation style: " + style)
    formatter = formatters[style.lower()]
    return formatter(paper)


def batch_cite(papers: list[Paper], style: str = "gbt7714") -> list[str]:
    """批量生成待核对的引文草稿列表

    Returns:
        编号引文列表，如 ["[1] 陈思和. ...", "[2] Benjamin. ..."]
    """
    return [
        f"[{i + 1}] {auto_cite(p, style)}"
        for i, p in enumerate(papers)
    ]
