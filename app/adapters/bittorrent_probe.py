import os

from app.adapters.qbittorrent_client import QBittorrentClient
from app.core.deduplicator import deduplicate_files
from app.core.models import ProbeResult
from app.core.normalizer import normalize_probe_result
from app.core.tagger import tag_file


def _filter_files(files: list[dict], filetype: str | None) -> list[dict]:
    if not filetype:
        return files
    return [file_entry for file_entry in files if file_entry.get("type") == filetype]


def _tag_files(files: list[dict]) -> list[dict]:
    return [tag_file(file_entry) for file_entry in files]


def _calculate_total_score(files: list[dict]) -> int:
    return sum(int(file_entry.get("score", 0)) for file_entry in files)


def _detect_type_from_path(path: str) -> str:
    path_lower = path.lower()

    if path_lower.endswith(".pdf"):
        return "pdf"
    if path_lower.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
        return "image"
    if path_lower.endswith((".txt", ".md", ".log")):
        return "text"
    if path_lower.endswith((".zip", ".rar", ".7z", ".tar", ".gz")):
        return "archive"
    return "other"


def _normalize_qbt_files(qbt_files: list[dict]) -> list[dict]:
    normalized: list[dict] = []

    for file_entry in qbt_files:
        name = file_entry.get("name") or ""
        size = int(file_entry.get("size", 0) or 0)

        normalized.append(
            {
                "path": name,
                "size": size,
                "type": _detect_type_from_path(name),
            }
        )

    return normalized


def _build_result(
    *,
    status: str,
    input_type: str,
    value: str,
    message: str,
    btih: str | None,
    files: list[dict],
    filetype: str | None,
    torrent_hash: str | None = None,
    torrent_name: str | None = None,
) -> dict:
    tagged_files = _tag_files(deduplicate_files(_filter_files(files, filetype)))
    total_score = _calculate_total_score(tagged_files)

    result = ProbeResult(
        status=status,
        input_type=input_type,
        value=value,
        adapter="bittorrent_probe",
        message=message,
        btih=btih,
        metadata_only=True,
        files=tagged_files,
        source="live-qbittorrent",
        extra={
            "filetype_filter": filetype,
            "deduplicated": True,
            "original_file_count": len(files),
            "final_file_count": len(tagged_files),
            "total_score": total_score,
            "torrent_hash": torrent_hash,
            "torrent_name": torrent_name,
        },
    )
    return normalize_probe_result(result)


def run_infohash_probe(infohash: str, filetype: str | None = None) -> dict:
    result = ProbeResult(
        status="error",
        input_type="infohash",
        value=infohash,
        adapter="bittorrent_probe",
        message="Direct infohash metadata probing is not implemented yet. Use magnet-based or .torrent-based live probing.",
        btih=infohash,
        metadata_only=True,
        files=[],
        source="live-qbittorrent",
        extra={
            "filetype_filter": filetype,
            "deduplicated": False,
            "original_file_count": 0,
            "final_file_count": 0,
            "total_score": 0,
        },
    )
    return normalize_probe_result(result)


def run_magnet_probe(magnet: str, btih: str | None = None, filetype: str | None = None) -> dict:
    if not btih:
        result = ProbeResult(
            status="error",
            input_type="magnet",
            value=magnet,
            adapter="bittorrent_probe",
            message="Missing btih for magnet probe.",
            btih=None,
            metadata_only=True,
            files=[],
            source="live-qbittorrent",
            extra={},
        )
        return normalize_probe_result(result)

    client = QBittorrentClient()

    try:
        client.login()
        client.add_magnet(magnet, paused=True)

        torrent = client.find_torrent_by_btih(btih)
        if not torrent:
            result = ProbeResult(
                status="warning",
                input_type="magnet",
                value=magnet,
                adapter="bittorrent_probe",
                message="Torrent was added, but metadata was not available yet.",
                btih=btih,
                metadata_only=True,
                files=[],
                source="live-qbittorrent",
                extra={
                    "filetype_filter": filetype,
                    "deduplicated": False,
                    "original_file_count": 0,
                    "final_file_count": 0,
                    "total_score": 0,
                },
            )
            return normalize_probe_result(result)

        torrent_hash = torrent.get("hash")
        qbt_files = client.list_files(torrent_hash)
        normalized_files = _normalize_qbt_files(qbt_files)

        return _build_result(
            status="ok",
            input_type="magnet",
            value=magnet,
            message="Live magnet metadata probe completed via qBittorrent.",
            btih=btih,
            files=normalized_files,
            filetype=filetype,
            torrent_hash=torrent_hash,
            torrent_name=torrent.get("name"),
        )

    except Exception as exc:
        result = ProbeResult(
            status="error",
            input_type="magnet",
            value=magnet,
            adapter="bittorrent_probe",
            message=f"Live magnet probe failed: {exc}",
            btih=btih,
            metadata_only=True,
            files=[],
            source="live-qbittorrent",
            extra={
                "filetype_filter": filetype,
                "deduplicated": False,
                "original_file_count": 0,
                "final_file_count": 0,
                "total_score": 0,
            },
        )
        return normalize_probe_result(result)


def run_torrent_file_probe(torrent_file_path: str, filetype: str | None = None) -> dict:
    if not os.path.exists(torrent_file_path):
        result = ProbeResult(
            status="error",
            input_type="torrent_file",
            value=torrent_file_path,
            adapter="bittorrent_probe",
            message=f".torrent file not found: {torrent_file_path}",
            btih=None,
            metadata_only=True,
            files=[],
            source="live-qbittorrent",
            extra={},
        )
        return normalize_probe_result(result)

    client = QBittorrentClient()

    try:
        client.login()
        client.add_torrent_file(torrent_file_path, paused=True)

        base_name = os.path.splitext(os.path.basename(torrent_file_path))[0]
        torrent = client.find_torrent_by_name(base_name)

        if not torrent:
            result = ProbeResult(
                status="warning",
                input_type="torrent_file",
                value=torrent_file_path,
                adapter="bittorrent_probe",
                message="Torrent file was added, but qBittorrent metadata was not available yet.",
                btih=None,
                metadata_only=True,
                files=[],
                source="live-qbittorrent",
                extra={
                    "filetype_filter": filetype,
                    "deduplicated": False,
                    "original_file_count": 0,
                    "final_file_count": 0,
                    "total_score": 0,
                },
            )
            return normalize_probe_result(result)

        torrent_hash = torrent.get("hash")
        qbt_files = client.list_files(torrent_hash)
        normalized_files = _normalize_qbt_files(qbt_files)

        return _build_result(
            status="ok",
            input_type="torrent_file",
            value=torrent_file_path,
            message="Live .torrent metadata probe completed via qBittorrent.",
            btih=torrent_hash,
            files=normalized_files,
            filetype=filetype,
            torrent_hash=torrent_hash,
            torrent_name=torrent.get("name"),
        )

    except Exception as exc:
        result = ProbeResult(
            status="error",
            input_type="torrent_file",
            value=torrent_file_path,
            adapter="bittorrent_probe",
            message=f"Live .torrent probe failed: {exc}",
            btih=None,
            metadata_only=True,
            files=[],
            source="live-qbittorrent",
            extra={
                "filetype_filter": filetype,
                "deduplicated": False,
                "original_file_count": 0,
                "final_file_count": 0,
                "total_score": 0,
            },
        )
        return normalize_probe_result(result)