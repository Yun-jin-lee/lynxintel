# Meeting Notes

## Project
Lynx OSINT for Tor and Jackett

## Current objective
Build a lightweight CLI-based OSINT probe engine that reduces dependence on opaque tooling and supports modular investigation workflows.

## Current development approach
The project is currently being built as a modular Python CLI application instead of a full torrent client replacement.

The current focus is on:
- clean architecture
- safe dry-run behavior where needed
- configuration through environment variables
- adapter-based design
- unit-tested foundations

## What has already been implemented

### Repository and collaboration
- GitLab repository created
- local workspace connected successfully
- initial project structure created
- collaborators can be added through GitLab members

### CLI and core logic
- CLI parser implemented
- command handlers implemented
- validators for infohash and magnet input implemented
- router implemented to select the correct adapter
- reporting layer implemented for terminal output

### BitTorrent and Jackett preparation
- placeholder BitTorrent probe adapter implemented
- placeholder Jackett adapter implemented
- dotenv-based configuration loading implemented
- Jackett environment configuration prepared through `.env.example` and `.env`

### Tor and Lynx preparation
- browse command added
- target validation added
- onion URL detection added
- Tor/Lynx dry-run adapter implemented
- prepared command output implemented
- local Lynx presence check implemented

## Current test status
The following tests currently pass:
- parser tests
- validator tests
- router tests
- Tor/Lynx adapter tests

Current result:
- 24 tests passed

## Current observed behavior

### Jackett
The Jackett integration layer is structurally implemented, but live API testing is still pending because no real Jackett API key is currently configured.

Current status:
- configuration loading works
- placeholder detection works
- adapter returns a controlled configuration error when the key is missing or still set to a placeholder value

### Tor/Lynx
The Tor/Lynx adapter currently works in dry-run mode.

Verified behavior:
- normal HTTP targets are accepted
- `.onion` targets are recognized
- the adapter selects the Tor/Lynx route correctly
- the prepared command is shown
- the code correctly reports that Lynx is not yet available on PATH in the current local environment

## Current blockers
- no real Jackett API key configured yet
- Lynx is not installed or not available on PATH on the current machine
- no live Tor browsing has been executed yet
- no live metadata-only BitTorrent probing has been implemented yet

## Architectural decisions made so far
- the project will remain CLI-first
- adapters should stay modular
- Jackett, Tor/Lynx, and BitTorrent probing should remain separate workflows
- environment-specific secrets should stay outside the repository
- the MVP should prioritize inspectability and testability over feature breadth

## Immediate next steps
1. commit current meeting notes and documentation
2. obtain a real Jackett API key and validate the live search path
3. install or configure Lynx so PATH detection succeeds
4. decide whether to prioritize:
   - real Jackett integration, or
   - live Tor/Lynx execution, or
   - BitTorrent metadata probing
5. continue expanding tests as new adapters become real implementations

## Talking points for the meeting
- the project already has a working modular skeleton
- parser, validators, routing, reporting, and config loading are working
- adapter-based architecture is already in place
- Jackett and Tor/Lynx are prepared structurally
- current work has been validated with unit tests
- the next step is moving from placeholders and dry-runs to live adapter execution