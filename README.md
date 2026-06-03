# LIRIS

Liris is a CLI-first utility designed for efficient text-based web browsing via Lynx and seamless torrent management through a qBittorrent backend. It serves as a glue layer to search, browse, and probe torrents directly from your terminal.

## Features

- **Lynx Integration**: Open URLs directly in the terminal or dump page content to stdout.
- **SearXNG Support**: Perform web searches using a self-hosted SearXNG instance and browse the results immediately.
- **qBittorrent Backend**: Add magnet links or torrent URLs directly to your remote or local qBittorrent instance.
- **Status Monitoring**: Get a quick snapshot of your active torrents and their progress.

## LIRIS Setup Guide

### Important System Requirements

You need **3 terminals** running simultaneously in WSL:

- **Terminal 1** = SearXNG
- **Terminal 2** = qBittorrent-nox
- **Terminal 3** = LIRIS commands

---

### Category 1: Clone or update Repository

If this is a fresh install, clone the repository using the following command.

```bash
git clone https://github.com/Yun-jin-lee/LIRIS
```

Otherwise follow the commands below

Only do this after the owner has merged the feature branch into main.

Navigate to your LIRIS project directory in WSL:

```bash
cd <your-path-to-LIRIS>
git checkout main
git pull origin main
```

**Verify:**

```bash
git branch
```

---

### Category 2: Create LIRIS Environment

In the LIRIS project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Convert windows line endings to linux and turn the `liris` file into an executable:

```bash
sed -i 's/\r$//' liris
chmod +x liris
```

**If the file is still named `Liris` (with capital L):**

```bash
mv Liris liris
sed -i 's/\r$//' liris
chmod +x liris
```

---

### Category 3: Create .env File

Create a `.env` file in the root of your LIRIS project directory with the following contents:

```bash
LYNX_BIN=lynx
QBITTORRENT_URL=http://localhost:8080
QBITTORRENT_USERNAME=admin
QBITTORRENT_PASSWORD=admin123
SEARXNG_URL=http://localhost:8888
```

**Important:** Only modify `QBITTORRENT_PASSWORD` if you use a different password locally.

---

### Category 4: Install WSL Packages

You typically only need to do this once:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-dev build-essential libxslt-dev libffi-dev libssl-dev qbittorrent-nox lynx
```

---

### Category 5: Install and Start qBittorrent-nox

qBittorrent-nox is installed via apt (completed in Category 4), not cloned.

#### Start qBittorrent-nox

**Terminal 2:**

```bash
qbittorrent-nox --webui-port=8080
```

#### Browser Check

Open in your browser:

```bash
http://localhost:8080
```

Log in with the default credentials found in the terminal and set your own password if needed.
**Update your LIRIS .env file with this password if you change it.**

---

### Category 6: Download SearXNG

Clone SearXNG in a separate directory (not in LIRIS):

```bash
cd ~
git clone https://github.com/searxng/searxng.git
cd searxng
```

---

### Category 7: Create SearXNG Virtual Environment

In `~/searxng`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -U setuptools wheel pyyaml msgspec typing-extensions pybind11
pip install --use-pep517 --no-build-isolation -e .
```

#### Verify Installation

```bash
python -c "import searx; print('searx import ok')"
```

---

### Category 8: Enable JSON in SearXNG

Open the settings file:

```bash
cd ~/searxng
nano ./searx/settings.yml
```

Find the `formats:` section and ensure it looks like this:

```yaml
formats:
  - html
  - json
```

#### Save in nano

- `Ctrl+O`
- `Enter`
- `Ctrl+X`

---

### Category 9: Start SearXNG

**Terminal 1:**

```bash
cd ~/searxng
source .venv/bin/activate
make run
```

#### Browser Check

Open in your browser:

```bash
http://localhost:8888
```

If you see the SearXNG homepage, everything is working.

---

### Category 10: Using LIRIS

**Terminal 3:**

```bash
cd <your-path-to-LIRIS>
source .venv/bin/activate
```

#### Search

```bash
./liris search "kuznyechik"
./liris search "kuznyechik" --provider google
./liris search "kuznyechik" --provider yandex
./liris search "kuznyechik" --provider baidu
```

#### Open URL

```bash
./liris open "https://en.wikipedia.org/wiki/Kuznyechik"
```

#### Check qBittorrent Status

```bash
./liris status
```

#### Add Torrent

```bash
./liris probe "https://releases.ubuntu.com/24.04/ubuntu-24.04.4-desktop-amd64.iso.torrent"
```

---

### Category 11: Terminal Summary

Quick reference for starting all three terminals:

#### Terminal 1: SearXNG

```bash
cd ~/searxng
source .venv/bin/activate
make run
```

#### Terminal 2: qBittorrent-nox

```bash
qbittorrent-nox --webui-port=8080
```

#### Terminal 3: LIRIS

```bash
cd <your-path-to-LIRIS>
source .venv/bin/activate
./liris search "kuznyechik"
```

---

### Category 12: Important Rules

- Every user must use their own local path in WSL
- Do **not** use `Ctrl+Z`
- Stop SearXNG with `Ctrl+C`
- Stop qBittorrent-nox with `Ctrl+C`
- Exit Lynx with `q`

---

### Category 13: Troubleshooting

#### Check if SearXNG is running

```bash
http://localhost:8888
```

#### Check if qBittorrent is running

```bash
http://localhost:8080
```

#### Check your current directory

```bash
pwd
```

#### Check if venv is activated

You should see `(.venv)` before your command prompt.

#### Check if .env file is correct

```bash
The `.env` file must be in the **root** of your LIRIS directory, not in `app/`.
```

```bash
--- status
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