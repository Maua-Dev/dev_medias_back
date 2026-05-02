from typing import Any, List


def scan_all_pages(table: Any, **scan_kwargs: Any) -> List[dict]:
    kwargs = dict(scan_kwargs)
    resp = table.scan(**kwargs)
    items: List[dict] = list(resp.get("Items", []))
    while "LastEvaluatedKey" in resp:
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
        resp = table.scan(**kwargs)
        items.extend(resp.get("Items", []))
    return items
