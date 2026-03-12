import json
import hashlib
from typing import Any, Callable, Optional, Self
from structures import Ingredient, Recipe
from utils import args_cast


class Hasher():
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
    
    def hash(self, content: dict[str, Any]) -> str:
        _hasher = hashlib.new(self.algorithm)
        _hasher.update(json.dumps(content, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        return _hasher.hexdigest()


class Registry():
    def __init__(self, kind: str, algorithm: str, content: Optional[dict[str, dict]]):
        self._hasher = Hasher(algorithm)
        
        match kind:
            case "INGREDIENT": self._cls = Ingredient
            case "RECIPE": self._cls = Recipe
            case _: raise NotImplementedError
        self._kind = kind
        
        self._content = {}
        if content:
            for key, val_dict in content.items():
                val = self._cls.from_dict(val_dict)
                _ = self._validate_entry(val, key)
                self._content[key] = val
    
    def _validate_entry(self, entry: Any, key: Optional[str]=None) -> str:
        if not isinstance(entry, self._cls):
            raise TypeError(
                f"Appended element must be {self._cls} type but {type(entry)} given"
                )
        entry_id = self._hasher(entry.as_dict())
        if key:
            if entry_id != key:
                raise ValueError(
                    f"Entry hash mismatch, given '{key}', expected '{entry_id}'"
                    )
        return entry_id
    
    def append(self, elem: Any):
        elem_id = self._validate_entry(elem)
        if elem_id not in self._content:
            self._content[elem_id] = elem
    
    def __getitem__(self, key: str):
        if key not in self._content:
            raise KeyError(f"No such {self._kind} '{key}' stored")
        return self._content[key]
    
    def __iter__(self):
        return iter(self._content.items())
    
    def filter(self, selector: Callable[[Any], bool]) -> list[str]:
        selection = []
        for key, ref in self:
            if selector(ref):
                selection.append(key)
        return selection
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "KIND": self._kind,
            "HASHER": self._hasher.algorithm,
            "CONTENT": {key: self._content[key].as_dict() for key in sorted(self._content)}
        }
    
    @classmethod
    def from_dict(cls, registry: dict[str, Any]) -> Self:
        return cls(**args_cast(REGISTRY_SCHEMA, registry))


REGISTRY_SCHEMA = {
    "KIND": ("kind", str),
    "HASHER": ("algorithm", str),
    "CONTENT": ("content", dict)
}
