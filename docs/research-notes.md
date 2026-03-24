# Research Notes

## Project direction
The project is being approached as a lightweight OSINT probe engine instead of a full torrent client replacement.

This means the focus is on:
- controlled input handling
- modular adapters
- metadata-oriented workflows
- inspectable and testable code
- CLI-first usage

## Why a custom lightweight engine
A custom lightweight engine is preferred over immediately forking a large existing client because:
- it reduces complexity
- it is easier to inspect
- it is easier to document for a meeting or academic setting
- it allows us to implement only the functions needed for the assignment
- it avoids inheriting unnecessary UI and client logic

## Current technical assumptions
The current design assumes the following:
- keyword search should be routed through a Jackett adapter
- infohash and magnet input should be routed through a BitTorrent metadata probe adapter
- Tor browsing should be handled separately through a Tor/Lynx adapter
- configuration should be loaded from environment variables
- local secrets must not be committed to Git

## Current implementation status
The following has already been built:
- repository and folder structure
- CLI parser
- validators for infohash and magnet input
- command execution flow
- router-based adapter selection
- adapter placeholders
- text reporting
- dotenv-based configuration loading
- unit tests

## Current limitations
The following parts are not implemented yet:
- live Jackett querying with a valid API key
- parsing live Jackett result content
- Tor integration
- Lynx execution wrapper
- qBittorrent integration
- metadata-only probe logic
- reporting export
- AI-based duplicate analysis

## Notes on Jackett
Current status:
- configuration support exists
- environment variable loading works
- the adapter correctly returns a placeholder or configuration error when no real API key is available

This means the integration layer is prepared, but live testing is still pending.

## Notes on Tor and Lynx
Tor and Lynx are planned as a separate adapter path rather than mixing them directly into the BitTorrent logic.

Reason:
- browsing and metadata probing are different workflows
- this keeps the code modular
- this makes testing and troubleshooting easier

## Notes on qBittorrent
qBittorrent is currently considered optional or secondary for the MVP.

Reason:
- the first milestone is a lightweight OSINT engine, not a full torrent client
- qBittorrent integration can later be used for management or workflow support
- it should not be the architectural core of the first prototype

## Notes for the meeting
Current talking points:
- the architecture is modular and CLI-first
- the codebase already supports parser, routing, validation, and configuration
- Jackett integration has been prepared structurally
- live Jackett testing still requires a valid API key
- the next technical priority is either live Jackett validation or Tor/Lynx adapter preparation

## Immediate next steps
1. commit current documentation
2. obtain or configure a real Jackett API key for live testing
3. decide whether the next implementation focus is Jackett or Tor/Lynx
4. start building the first real adapter instead of placeholders