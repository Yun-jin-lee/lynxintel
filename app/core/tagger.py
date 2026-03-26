def tag_file(file_entry: dict) -> dict:
    path = (file_entry.get("path") or "").lower()
    file_type = (file_entry.get("type") or "").lower()

    tags: list[str] = []

    if file_type in {"pdf", "word", "powerpoint", "excel", "text", "document"}:
        tags.extend(["document", "interesting"])

    if file_type == "pdf":
        tags.append("pdf")

    if file_type == "word":
        tags.append("word_document")

    if file_type == "powerpoint":
        tags.append("presentation")

    if file_type == "excel":
        tags.append("spreadsheet")

    if file_type == "image":
        tags.append("image")

    if file_type == "archive":
        tags.extend(["archive", "interesting"])

    if file_type == "disk_image":
        tags.extend(["disk_image", "interesting"])

    if file_type == "executable":
        tags.extend(["executable", "interesting"])

    if file_type == "apk":
        tags.extend(["apk", "mobile_package", "interesting"])

    if file_type == "script":
        tags.extend(["script", "interesting"])

    if file_type in {"html", "json", "xml", "csv"}:
        tags.extend(["structured_data", "interesting"])

    if "report" in path or "evidence" in path or "case" in path or "incident" in path:
        tags.append("high_value_candidate")

    if any(ext in path for ext in [".zip", ".rar", ".7z", ".tar", ".gz"]):
        tags.append("compressed")

    score = 0

    if "interesting" in tags:
        score += 2
    if "high_value_candidate" in tags:
        score += 3
    if "compressed" in tags:
        score += 1
    if "executable" in tags:
        score += 2
    if "apk" in tags:
        score += 2
    if "disk_image" in tags:
        score += 1

    tagged_entry = dict(file_entry)
    tagged_entry["tags"] = sorted(set(tags))
    tagged_entry["score"] = score
    return tagged_entry