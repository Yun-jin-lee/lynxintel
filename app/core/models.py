from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProbeResult:
    status: str
    input_type: str
    value: str
    adapter: str
    message: str
    btih: str | None = None
    metadata_only: bool = True
    files: list[dict[str, Any]] = field(default_factory=list)
    source: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)