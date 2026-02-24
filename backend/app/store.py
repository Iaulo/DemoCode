from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import itertools


@dataclass
class Item:
    id: int
    title: str
    done: bool = False


class InMemoryStore:
    """Store simple para tener lógica testeable (ideal para unit tests)."""
    def __init__(self) -> None:
        self._items: Dict[int, Item] = {}
        self._ids = itertools.count(1)

    def list(self, q: Optional[str] = None) -> List[dict]:
        items = list(self._items.values())
        if q:
            q_low = q.lower()
            items = [it for it in items if q_low in it.title.lower()]
        return [asdict(i) for i in sorted(items, key=lambda x: x.id)]

    def create(self, title: str) -> dict:
        title = (title or "").strip()
        if not title:
            raise ValueError("title is required")
        new_id = next(self._ids)
        item = Item(id=new_id, title=title, done=False)
        self._items[new_id] = item
        return asdict(item)

    def toggle(self, item_id: int) -> dict:
        if item_id not in self._items:
            raise KeyError("not found")
        it = self._items[item_id]
        it.done = not it.done
        return asdict(it)

    def delete(self, item_id: int) -> None:
        if item_id not in self._items:
            raise KeyError("not found")
        del self._items[item_id]
