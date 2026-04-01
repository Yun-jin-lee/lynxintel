# LIRIS — Lynx Investigation Reconnaissance Information System

**LIRIS** is a CLI-first, open-source OSINT toolchain focused on **metadata-only** investigations across BitTorrent-related sources, with **auditability**, **secure defaults**, and **operational reproducibility** as first-class goals.

**Acronym**
- **L** = Lynx
- **I** = Investigation
- **R** = Reconnaissance
- **I** = Information
- **S** = System

> Design intent: enable intelligence gathering **without downloading files**, reduce reliance on black-box OSINT platforms, and provide transparent tooling suitable for controlled investigative environments.

---

## Why LIRIS

Many OSINT workflows depend on:
- commercial scrapers;
- opaque open-source tooling (unclear behavior, supply-chain risk);
- black-box platforms with limited auditability.

At the same time, **BitTorrent metadata** is often an underused OSINT signal source:
- decentralized discovery (DHT / BEP 0005);
- metadata-driven identifiers (magnets, infohash);
- indexer gateways (Jackett / Torznab).

LIRIS aims to combine these into a **reviewable** and **operator-friendly** CLI workflow, with **Tor support** where appropriate and strict attention to legal/ethical boundaries.

---

## Core Principles

- **Metadata-only by default**: no content download, no seeding/leeching.
- **Transparent + auditable**: clear data flows, explicit configuration, reproducible outputs.
- **Secure-by-design**: safe defaults, controlled logging, minimized retention.
- **CLI-native**: predictable automation, scripting, and composability.
- **PowerShell-friendly**: object output and pipeline patterns (module approach).

---

## Current Scope (our direction)

### Search & Collection
- **Jackett (Torznab) integration** for indexer-based searches
- **Tor routing support** (SOCKS5), with safeguards to prevent clearnet leaks
- **Google-like operators (subset)** mapped to supported query filters

### Processing & Analysis
- Metadata enrichment (e.g., trackers, tags, sizes, filenames where available)
- Deduplication / clustering (heuristics-first; optional ML later)
- Minimal, controlled caching to balance performance and retention constraints

### Reporting
- Structured outputs suitable for investigations
- Export-oriented reporting (planned): evidence tables and highlighted results

---

## Primary OSINT Scenarios

1. **Keyword metadata sweep (indexer-first + enrichment)**
   - Query via Jackett/Torznab
   - Enrich with additional metadata and clustering
   - Produce a case-ready result set

2. **Reverse image correlation over torrent metadata (no downloads)**
   - Input: image fingerprint (e.g., perceptual hash)
   - Match: against known/collected metadata indices
   - Output: candidate torrents/collections that likely contain matching images

3. **Infrastructure footprint mapping**
   - Tor-based discovery of mentions/handles/keywords
   - Correlate findings with torrent metadata sources
   - Summarize overlaps, clusters, and timelines

---

## Planned / Future Work

These are **not required for the initial concept**, but are part of the roadmap:

- **qBittorrent integration** (headless / WebUI API) for controlled metadata retrieval and enrichment
- **Tixati integration** (headless / HTTPS-enabled operations) where suitable
- Optional exploration of **I2P** (value vs. complexity/performance trade-offs)
- Relevance assessment (scope-guarded): **Usenet** (possibly), **eMule/DC++/IRC** (likely out of scope)

---

## What LIRIS is NOT

- Not a tool for piracy or downloading content.
- Not a “fully stealth” botnet-style crawler.
- Not a replacement for legal review, policy, and operator judgment.

---

## High-Level Architecture (concept)

```text
LIRIS CLI / PowerShell Module
│
├── Search Layer
│   ├── Jackett (Torznab) client
│   └── Lynx-over-Tor client (for text-based recon)
│
├── P2P / Metadata Layer
│   ├── DHT scanning (BEP 0005) (planned/optional per phase)
│   ├── Metadata retrieval (conceptual: ut_metadata)
│   └── Deduplication / clustering engine
│
├── Security & OpSec
│   ├── Safe defaults + config hardening
│   ├── Rate limiting / retries / backoff
│   └── Audit logging (minimal & controlled)
│
└── Reporting
    ├── Structured exports
    └── DOCX/PPTX generation (planned)
```

---

## Installation

> TBD — project is in early development.
> This section will include:
> - supported OS versions
> - PowerShell module installation
> - configuration for Tor + Jackett
> - example commands

---

## Usage

> TBD — placeholder examples (to be replaced once commands stabilize):

```bash
# Example (future): search via Jackett, output as JSON objects
liris search "keyword" --tor --jackett http://127.0.0.1:9117 --json

# Example (future): run a scenario workflow
liris scenario keyword-sweep --query "..." --report out.docx
```

PowerShell usage will follow pipeline-first patterns:

```powershell
# Example (future): object output, then export
Search-LirisTorrent -Query "keyword" | Export-LirisReport -Path .\report.docx
```

---

## Security, Legal, and Ethics

LIRIS is designed around:
- **least data**: collect only what is necessary for the stated investigative purpose
- **controlled logging**: avoid sensitive logging by default; provide explicit opt-in diagnostics
- **rate limiting and abuse prevention**: backoff, caps, and guardrails
- **supply-chain awareness**: reviewable dependencies and reproducible builds (planned)

Operators are responsible for using LIRIS within applicable laws, policies, and authorization boundaries.

---

## Contributing

Contributions are welcome, especially around:
- PowerShell module design (cmdlets, pipeline patterns)
- Jackett/Torznab client robustness (retries, backoff, parsing)
- Test harnesses and reproducible benchmarking
- Documentation and threat modeling

> Contribution guidelines, code of conduct, and security disclosure process: **TBD**.

---

## License

**TBD** — choose an OSI-approved license (e.g., MIT/Apache-2.0/GPL-3.0) consistent with the intended deployment context.

---

## Contact / Maintainers

- (Team 4)  
- Maintainer list: **TBD**