from datetime import datetime, timezone


def serialize(doc):
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "text": doc.get("text", ""),
        "created_at": doc["created_at"].isoformat(),
    }


def validate(data, title_max_length):
    title = data.get("title")
    text = data.get("text", "")
    if not isinstance(title, str) or not title.strip():
        return None, "title is required"
    if len(title) > title_max_length:
        return None, f"title exceeds {title_max_length} characters"
    if not isinstance(text, str):
        return None, "text must be a string"
    return {
        "title": title.strip(),
        "text": text,
        "created_at": datetime.now(timezone.utc),
    }, None
