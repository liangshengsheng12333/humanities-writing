"""Retained literature adapter; not live-tested. Configuration readiness does not prove connectivity."""
from __future__ import annotations
import sys, os, json
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.schema import Paper, SearchResult
from lib.utils import env_get, parse_year

SEARCH_URL = "https://api.core.ac.uk/v3/search/works"


def is_available() -> bool:
    """CORE适配器可加载；访问条件、费用及接口需实测"""
    return True


def search(query: str, limit: int = 20) -> SearchResult:
    """搜索 CORE"""
    api_key = env_get("CORE_API_KEY")

    params = {
        "q": query,
        "limit": str(min(limit, 100)),
    }

    url = SEARCH_URL + "?" + urllib.parse.urlencode(params)
    headers = {
        "User-Agent": "humanities-thesis-skill/1.0",
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        papers: list[Paper] = []
        results = data.get("results", [])

        for item in results[:limit]:
            title = item.get("title") or ""
            if not title:
                continue

            # 作者
            authors = []
            for author in item.get("authors", []):
                if isinstance(author, dict):
                    name = author.get("name", "")
                elif isinstance(author, str):
                    name = author
                else:
                    name = ""
                if name:
                    authors.append(name)

            # 年份
            year = item.get("yearPublished") or 0
            if not year:
                year = parse_year(str(item.get("publishedDate", "")))

            # URL 和 DOI
            doi = ""
            for ext_id in (item.get("identifiers") or []):
                if isinstance(ext_id, str) and "doi.org" in ext_id:
                    doi = ext_id.replace("https://doi.org/", "").replace("http://doi.org/", "")
                    break

            url_paper = ""
            links = item.get("links") or []
            for link in links:
                if isinstance(link, dict) and link.get("type") == "reader":
                    url_paper = link.get("url", "")
                    break
            if not url_paper:
                fulltext_urls = item.get("sourceFulltextUrls") or []
                url_paper = item.get("downloadUrl") or (fulltext_urls[0] if fulltext_urls else "")
            link_kind = "fulltext" if url_paper else "record"
            if not url_paper and doi:
                url_paper = f"https://doi.org/{doi}"

            # 期刊
            venue = ""
            journals = item.get("journals") or []
            if journals and isinstance(journals[0], dict):
                venue = journals[0].get("title", "")

            # 摘要
            abstract = item.get("abstract") or ""
            if len(abstract) > 500:
                abstract = abstract[:500] + "..."

            # 语言
            language = item.get("language", {})
            if isinstance(language, dict):
                language = language.get("code", "")
            elif not isinstance(language, str):
                language = ""

            papers.append(
                Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    url=url_paper,
                    source="CORE",
                    venue=venue,
                    abstract=abstract,
                    doi=doi,
                    citation_count=item.get("citationCount") or 0,
                    language=language,
                    link_kind=link_kind,
                )
            )

        total = data.get("totalHits", len(papers))
        return SearchResult(
            query=query, source="CORE", papers=papers, total_found=total
        )
    except Exception as e:
        return SearchResult(query=query, source="CORE", error=str(e))


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "deconstruction Chinese literature"
    result = search(q)
    print(result.to_json())
