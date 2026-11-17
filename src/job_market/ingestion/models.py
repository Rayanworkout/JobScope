from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Job:
    """
    Class representing a job object to interact with it. Methods enable us
    to convert the API reponse to this unified format that we will then insert
    into the database
    """
    source: str
    source_guid: str
    title: str
    company_name: str
    raw_data: dict[str, Any]

    @classmethod
    def from_himalayas(cls, data: dict[str, Any]) -> "Job":  # noqa: UP037
        return cls(
            source="himalayas",
            source_guid=data["guid"],
            title=data["title"],
            company_name=data["companyName"],
            raw_data=data,
        )

    def __str__(self) -> str:
        return f"[{self.source}] {self.title} at {self.company_name}"
