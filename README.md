# LIRIS

CLI-first tool for:
- opening web pages as text via Lynx
- keyword searching through a text-friendly search page
- probing magnet links through qBittorrent

## Commands

```bash
python -m app.main open "https://en.wikipedia.org/wiki/Kuznyechik"
python -m app.main search "kuznyechik"
python -m app.main probe "magnet:?xt=urn:btih:..."
python -m app.main status


## 14. Installeren
In je project:

```bash id="inst001"
pip install -r requirements.txt