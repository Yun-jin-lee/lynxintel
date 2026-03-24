# Architecture

## Project goal
Build a lightweight CLI-based OSINT probe engine that supports:
- text-based Tor browsing through Lynx
- centralized keyword search through Jackett
- BitTorrent metadata-oriented probing through infohash and magnet inputs

The main design goal is to reduce dependence on opaque tooling by using a modular, inspectable, CLI-first codebase.

## Current MVP scope
The current MVP includes:
- CLI argument parsing
- validation for keyword, infohash, and magnet input
- routing logic
- adapter skeletons
- text-based reporting
- local configuration through `.env`
- unit tests for parser, validators, and router

The current MVP does not yet include:
- reverse image search
- DOCX or PPTX reporting
- AI analysis
- I2P support
- full qBittorrent replacement
- advanced DHT crawling
- live Jackett production search with a real API key
- live Tor/Lynx browsing integration

## High-level modules

### CLI layer
Responsible for parsing user input and dispatching commands.

Files:
- `app/main.py`
- `app/cli/parser.py`
- `app/cli/commands.py`

### Core layer
Responsible for routing and shared logic.

Files:
- `app/core/router.py`
- `app/core/models.py`
- `app/core/normalizer.py`
- `app/core/deduplicator.py`

### Adapter layer
Responsible for interacting with external tools and services.

Files:
- `app/adapters/bittorrent_probe.py`
- `app/adapters/jackett_client.py`
- `app/adapters/tor_lynx_client.py`
- `app/adapters/qbittorrent_client.py`

### Reporting layer
Responsible for presenting results to the operator.

Files:
- `app/reporting/text_reporter.py`
- `app/reporting/json_reporter.py`
- `app/reporting/docx_reporter.py`

### Configuration layer
Responsible for loading local runtime configuration from environment variables.

Files:
- `app/config.py`
- `.env.example`
- `.env`

## Current execution flow

### Keyword search flow
User input  
-> CLI parser  
-> search command  
-> input validation  
-> router  
-> Jackett adapter  
-> text reporter

### Infohash probe flow
User input  
-> CLI parser  
-> probe command  
-> input validation  
-> router  
-> BitTorrent probe adapter  
-> text reporter

### Magnet probe flow
User input  
-> CLI parser  
-> probe command  
-> input validation  
-> btih extraction  
-> router  
-> BitTorrent probe adapter  
-> text reporter

## Design principles
- keep the engine lightweight
- keep adapters modular
- separate validation, routing, execution, and reporting
- prefer metadata-oriented workflows where possible
- keep secrets out of the repository
- make the code easy to test and extend

## Current status
Implemented:
- parser
- validators
- command handlers
- router
- adapter skeletons
- text reporting
- dotenv-based configuration loading
- unit tests for parser, validators, and router

Planned next:
- real Jackett integration with live API key
- Tor/Lynx adapter preparation
- BitTorrent metadata probing implementation
- result normalization
- duplicate handling
- reporting expansion