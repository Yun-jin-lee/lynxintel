from app.core.tagger import tag_file


def test_tag_file_adds_document_tags():
    file_entry = {"path": "docs/report.pdf", "size": 100, "type": "pdf"}
    result = tag_file(file_entry)

    assert "document" in result["tags"]
    assert "interesting" in result["tags"]
    assert "high_value_candidate" in result["tags"]
    assert result["score"] >= 1


def test_tag_file_adds_archive_tags():
    file_entry = {"path": "media/archive.zip", "size": 200, "type": "archive"}
    result = tag_file(file_entry)

    assert "archive" in result["tags"]
    assert "compressed" in result["tags"]
    assert result["score"] >= 1


def test_tag_file_adds_image_tag():
    file_entry = {"path": "images/photo.jpg", "size": 300, "type": "image"}
    result = tag_file(file_entry)

    assert "image" in result["tags"]