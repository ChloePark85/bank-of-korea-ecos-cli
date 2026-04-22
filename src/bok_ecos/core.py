import os
import json
import sys
from typing import Any, Dict

import requests

BASE_URL = os.environ.get("BOK_ECOS_BASE_URL", "https://ecos.bok.or.kr/api")

class EcosClient:
    def __init__(self, api_key: str | None = None, lang: str = "kr") -> None:
        self.api_key = api_key or os.environ.get("BOK_API_KEY") or os.environ.get("ECOS_API_KEY")
        if not self.api_key:
            raise ValueError("Missing API key. Set BOK_API_KEY or pass api_key explicitly.")
        self.lang = lang

    def _get(self, path: str) -> Dict[str, Any]:
        url = f"{BASE_URL}{path}"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def table_list(self, start: int = 1, end: int = 1000) -> Dict[str, Any]:
        path = f"/StatisticTableList/{self.api_key}/json/{self.lang}/{start}/{end}/"
        return self._get(path)

    def series(self, stat_code: str, cycle: str, start_date: str, end_date: str,
               start: int = 1, end: int = 1000) -> Dict[str, Any]:
        cycle = cycle.upper()
        if cycle not in {"A", "S", "Q", "M", "D"}:
            raise ValueError("cycle must be one of A,S,Q,M,D (Annual/Semiannual/Quarterly/Monthly/Daily)")
        path = f"/StatisticSearch/{self.api_key}/json/{self.lang}/{start}/{end}/{stat_code}/{cycle}/{start_date}/{end_date}/"
        return self._get(path)


def print_json(data: Dict[str, Any]) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
