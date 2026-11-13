"""查询预处理

将用户的自然语言搜索词优化为更适合学术数据库检索的形式。
处理中英文混合、理论家名字中英对照、常见缩写展开等。
"""
from __future__ import annotations
import re


# 常见理论家中英文对照（人文社科高频）
_SCHOLAR_MAP: dict[str, str] = {
    "福柯": "Foucault",
    "德里达": "Derrida",
    "本雅明": "Benjamin",
    "阿甘本": "Agamben",
    "巴特勒": "Butler",
    "阿伦特": "Arendt",
    "南希": "Nancy",
    "布朗肖": "Blanchot",
    "阿多诺": "Adorno",
    "萨义德": "Said",
    "巴巴": "Bhabha",
    "斯皮瓦克": "Spivak",
    "鲁迅": "Lu Xun",
    "布尔迪厄": "Bourdieu",
    "拉康": "Lacan",
    "列维纳斯": "Levinas",
    "德勒兹": "Deleuze",
    "齐泽克": "Žižek",
    "海德格尔": "Heidegger",
    "哈贝马斯": "Habermas",
    "韦伯": "Weber",
    "涂尔干": "Durkheim",
    "葛兰西": "Gramsci",
    "霍克海默": "Horkheimer",
    "克里斯蒂娃": "Kristeva",
    "索绪尔": "Saussure",
    "巴赫金": "Bakhtin",
    "本尼迪克特·安德森": "Benedict Anderson",
    "莫雷蒂": "Moretti",
}

# 常见学术缩写展开
_ABBREV_MAP: dict[str, str] = {
    "文革": "文化大革命",
    "五四": "五四运动",
    "后殖民": "后殖民主义",
    "解构": "解构主义",
    "现象学": "现象学 phenomenology",
}


def _extract_chinese(text: str) -> list[str]:
    """提取中文词汇（连续中文字符）"""
    return re.findall(r"[\u4e00-\u9fff]+", text)


def _extract_english(text: str) -> list[str]:
    """提取英文词汇"""
    return re.findall(r"[a-zA-ZÀ-ÿ]+(?:\s+[a-zA-ZÀ-ÿ]+)*", text)


def expand_query(query: str) -> dict[str, str]:
    """返回原始查询和小型字典扩展建议，不丢弃未映射片段或数字。"""
    concepts = {
        "创伤": "trauma", "叙事": "narrative", "现代性": "modernity",
        "暴力": "violence", "记忆": "memory", "身体": "body", "空间": "space",
        "权力": "power", "主体": "subjectivity", "他者": "other alterity",
        "共同体": "community", "寓言": "allegory", "废墟": "ruin",
    }
    mapping = {**_SCHOLAR_MAP, **concepts}
    for word, expanded in _ABBREV_MAP.items():
        english = _extract_english(expanded)
        if english:
            mapping[word] = " ".join(english)
    # Only replace complete contiguous Chinese tokens; unknown content remains intact.
    en = re.sub(r"[\u4e00-\u9fff]+", lambda m: mapping.get(m.group(), m.group()), query)
    return {"zh": query.strip(), "en": en.strip(), "original": query}


def suggest_queries(query: str) -> list[str]:
    """基于用户查询推荐多个搜索变体

    返回1至5个搜索建议，用于不同数据库；均须人工核对。
    """
    expanded = expand_query(query)
    suggestions = [expanded["original"]]

    if expanded["zh"] != expanded["original"]:
        suggestions.append(expanded["zh"])
    if expanded["en"] != expanded["original"]:
        suggestions.append(expanded["en"])

    # 如果查询包含理论家名字，生成"理论家+研究对象"的组合
    chinese_words = _extract_chinese(query)
    scholars_found = [w for w in chinese_words if w in _SCHOLAR_MAP]
    non_scholars = [w for w in chinese_words if w not in _SCHOLAR_MAP]

    if scholars_found and non_scholars:
        # 英文版：理论家英文名+研究对象
        for scholar in scholars_found:
            en_name = _SCHOLAR_MAP[scholar]
            en_suggestion = f"{en_name} {' '.join(non_scholars)}"
            if en_suggestion not in suggestions:
                suggestions.append(en_suggestion)

    return suggestions[:5]
