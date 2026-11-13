"""环境变量读取与日期解析工具"""
from __future__ import annotations
import os
import re


# ── 环境变量 ──────────────────────────────────────────────

def env_get(key: str, default: str = "") -> str:
    """读取环境变量，支持 .env 文件回退"""
    val = os.environ.get(key, "")
    if val:
        return val
    # Explicit path or this skill's scripts/.env; never guess a cwd project configuration.
    explicit = os.environ.get("HUMANITIES_WRITING_CONFIG", "")
    env_candidates = [os.path.abspath(explicit)] if explicit else [
        os.path.join(os.path.dirname(__file__), "..", ".env")]
    for env_path in env_candidates:
        if os.path.isfile(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            if k.strip() == key:
                                return v.strip().strip('"').strip("'")
            except OSError:
                pass
    return default


# ── 日期解析 ──────────────────────────────────────────────

_YEAR_PATTERN = re.compile(r"(19|20)\d{2}")


def parse_year(text: str) -> int:
    """从文本中提取四位年份，失败返回 0"""
    if not text:
        return 0
    m = _YEAR_PATTERN.search(text)
    return int(m.group()) if m else 0
