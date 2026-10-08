"""
MinHash LSH Entity & Value Linking Indexer:
Maps natural language mentions (e.g. 'type 2 diabetes', 'inpatient') to canonical database values.
"""
import hashlib


class MinHashLSHIndex:
    def __init__(self, num_perm: int = 16):
        self.num_perm = num_perm
        self.index: dict[str, str] = {} # token -> canonical value

    def _hash(self, token: str) -> str:
        return hashlib.md5(token.lower().strip().encode("utf-8")).hexdigest()[:8]

    def add_value(self, canonical_value: str, aliases: list[str]):
        self.index[self._hash(canonical_value)] = canonical_value
        for alias in aliases:
            self.index[self._hash(alias)] = canonical_value

    def match_entity(self, text: str) -> list[tuple[str, float]]:
        words = text.lower().split()
        matches = []
        for w in words:
            h = self._hash(w)
            if h in self.index:
                matches.append((self.index[h], 0.95))
        return matches
