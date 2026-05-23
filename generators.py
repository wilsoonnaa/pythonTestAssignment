def generate_delta(config: dict, patched: dict) -> dict:
    additions = []
    deletions = []
    updates = []

    for key in patched:
        if key not in config:
            additions.append({
                "key": key,
                "value": patched[key],
            })
        elif patched[key] != config[key]:
            updates.append({
                "key": key,
                "value": config[key],
                "to": patched[key],
            })
        
    for key in config:
        if key not in patched:
            deletions.append(key)

    return {
        "additions": additions,
        "deletions": deletions,
        "updates": updates,
    }