# LIRIS

Liris is a CLI-first utility designed for efficient text-based web browsing via Lynx and seamless torrent management through a qBittorrent backend. It serves as a glue layer to search, browse, and probe torrents directly from your terminal.

## Features

- **Lynx Integration**: Open URLs directly in the terminal or dump page content to stdout.
- **SearXNG Support**: Perform web searches using a self-hosted SearXNG instance and browse the results immediately.
- **qBittorrent Backend**: Add magnet links or torrent URLs directly to your remote or local qBittorrent instance.
- **Status Monitoring**: Get a quick snapshot of your active torrents and their progress.

## Configuration

Create a `.env` file in the root directory to configure the application:

```text
LYNX_BIN=lynx
QBITTORRENT_URL=http://localhost:8080
QBITTORRENT_USERNAME=admin
QBITTORRENT_PASSWORD=adminadmin
SEARXNG_URL=http://localhost:8888
```

## Usage

Liris provides a simple sub-command structure:

### 1. Browse the Web
Open a URL in interactive mode:
```bash
python main.py open https://example.com
```

Dump the text content of a page:
```bash
python main.py open https://example.com --dump
```

### 2. Search
Search the web via SearXNG and select a link to open in Lynx:
```bash
python main.py search "query string" --provider google
```

Show unique first-page results from multiple SearXNG engines:
```bash
python main.py search "query string" --unique
```

Or use the root wrapper script directly:
```bash
./liris search "query string" --unique
```

### 3. Torrent Management
Add a magnet link to your qBittorrent client:
```bash
python main.py probe "magnet:?xt=urn:btih:..."
```

Check the status of your torrents:
```bash
python main.py status
```

## Roadmap & Future Development

Liris is currently in active development. We aim to bridge the gap between terminal-based information discovery and media acquisition.

### Planned Features

- **Jackett Integration**: 
    - Full indexing support to search across multiple private and public torrent trackers directly from the CLI.
    - Automated mapping of Jackett search results to the `probe` command.
- **Improved Caching**: Implementation of a local cache for search results to reduce latency and load on your SearXNG instance.
- **Interactive UI Enhancements**:
    - Replacing basic `input()` prompts with a more robust library like `prompt_toolkit` for better navigation.
    - Adding support for saved "searches" or "bookmarks" in a local JSON config.
- **Config Management**: Ability to switch between multiple `.env` profiles (e.g., `prod` vs `dev` or `home` vs `work`).

### Jackett Integration Details
The integration will follow a service-oriented pattern similar to the existing SearXNG service:

1. **New Adapter**: An `app/adapters/jackett_client.py` will be implemented to interface with the Jackett API.
2. **Search Pipeline**: 
    - The `search` command will be updated to optionally include a `--tracker` flag.
    - Results returned from Jackett will be parsed and filtered, allowing users to pipe magnet links directly into the `probe` service.
3. **Configuration**: New environment variables will be added to the `.env` schema:
    ```text
    JACKETT_URL=http://localhost:9117
    JACKETT_API_KEY=your_api_key_here
    ```

## Requirements

- Python 3.9+
- [Lynx](https://lynx.invisible-island.net/) (Text-based web browser)
- A running [SearXNG](https://github.com/searxng/searxng) instance (for search functionality)
- A running [qBittorrent](https://www.qbittorrent.org/) instance (for torrent functionality)

## Installation

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install requests python-dotenv
   ```
3. Set up your `.env` file and run `python main.py --help` to get started.

## Contributions
Contributions are welcome! If you are interested in accelerating the Jackett integration or adding features, please check the `app/services/` directory to see how existing services are structured and feel free to submit a pull request.