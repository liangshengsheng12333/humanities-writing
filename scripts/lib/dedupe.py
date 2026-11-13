"""保守去重：DOI 优先；缺 DOI 时须由同标题、作者和年份共同支持。"""
from __future__ import annotations
from dataclasses import replace
import re
import unicodedata

from .schema import Paper


def _normalize(text: str) -> str:
    """标准化文本用于比较：去除空白、标点、统一大小写"""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[^\w]", "", text)  # 去掉所有非字母数字字符
    return text.lower().strip()


def _title_key(paper: Paper) -> str:
    """从标题生成比较用的 key"""
    return _normalize(paper.title)


def _doi_key(paper: Paper) -> str | None:
    """从 DOI 生成比较用的 key"""
    if not paper.doi:
        return None
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "",
                  paper.doi.lower().strip())


def _merge_papers(existing: Paper, new: Paper) -> Paper:
    """保留首次非空字段与冲突线索，不修改输入记录。"""
    conflicts = list(dict.fromkeys(existing.metadata_conflicts + new.metadata_conflicts))
    fields = {}
    for field in ("title", "authors", "year", "venue", "language", "document_type", "record_type"):
        left, right = getattr(existing, field), getattr(new, field)
        if left and right and left != right:
            note = f"{field}: {left!r} <> {right!r}"
            if note not in conflicts:
                conflicts.append(note)
        fields[field] = left or right
    return replace(existing, **fields,
                   doi=existing.doi or new.doi,
                   url=existing.url or new.url,
                   link_kind=existing.link_kind if existing.url else new.link_kind,
                   source=", ".join(dict.fromkeys(
                       part.strip() for value in (existing.source, new.source)
                       for part in value.split(",") if part.strip())),
                   abstract=max((existing.abstract, new.abstract), key=len),
                   keywords=list(dict.fromkeys(existing.keywords + new.keywords)),
                   citation_count=max(existing.citation_count, new.citation_count),
                   metadata_conflicts=conflicts)


def dedupe(papers: list[Paper]) -> list[Paper]:
    """不同非空 DOI 不合并；缺 DOI 或多个候选时宁可保留。"""
    def signature(paper: Paper):
        return (_title_key(paper), paper.year, tuple(_normalize(a) for a in paper.authors))

    known_dois: dict[tuple, set[str]] = {}
    for paper in papers:
        doi = _doi_key(paper)
        if doi:
            known_dois.setdefault(signature(paper), set()).add(doi)
    result: list[Paper] = []
    for paper in papers:
        doi_k = _doi_key(paper)
        title_k = _title_key(paper)
        if not title_k:
            continue
        candidates = [i for i, old in enumerate(result)
                      if doi_k and doi_k == _doi_key(old)]
        if not candidates:
            for i, old in enumerate(result):
                old_doi = _doi_key(old)
                if doi_k and old_doi:
                    continue
                if len(known_dois.get(signature(paper), set())) > 1:
                    continue
                if (title_k == _title_key(old) and paper.year and paper.year == old.year
                        and paper.authors and old.authors
                        and [_normalize(a) for a in paper.authors]
                        == [_normalize(a) for a in old.authors]):
                    candidates.append(i)
        if len(candidates) == 1:
            idx = candidates[0]
            result[idx] = _merge_papers(result[idx], paper)
        else:
            result.append(replace(paper, authors=list(paper.authors), keywords=list(paper.keywords),
                                  metadata_conflicts=list(paper.metadata_conflicts)))
    return result
