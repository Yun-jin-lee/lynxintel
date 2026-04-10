from dataclasses import dataclass, field

@dataclass
class SearchRequest:
    provider: str
    keyword: str
    use_case: str | None = None
    site: str | None = None
    filetype: str | None = None
    exact_phrase: str | None = None
    exclude_terms: list[str] = field(default_factory=list)
    additional_terms: list[str] = field(default_factory=list)
    language: str | None = None
    region: str | None = None


@dataclass
class SearchResult:
    status: str
    provider: str
    adapter: str
    use_case: str | None
    query: str
    manual_search_url: str
    message: str
    filters: dict = field(default_factory=dict)
    results: list | None = None
    raw: dict | None = None