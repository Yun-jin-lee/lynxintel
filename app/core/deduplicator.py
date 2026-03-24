def deduplicate_files(files: list[dict]) -> list[dict]:
    seen: set[tuple] = set()
    deduplicated: list[dict] = []

    for file_entry in files:
        key = (
            file_entry.get("path"),
            file_entry.get("size"),
            file_entry.get("type"),
        )

        if key in seen:
            continue

        seen.add(key)
        deduplicated.append(file_entry)

    return deduplicated