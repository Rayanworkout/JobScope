import datetime
from dataclasses import dataclass
from typing import Any

from ..core.helpers.expiration import timestamp_is_expired
from ..core.helpers.parsing import html_to_text


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
    is_expired: bool
    description: str
    raw_data: dict[str, Any]
    db_id: int | None = None
    updated_at: datetime.datetime | None = None
    created_at: datetime.datetime | None = None

    @classmethod
    def from_himalayas(cls, data: dict[str, Any]) -> "Job":  # noqa: UP037
        return cls(
            source="himalayas",
            source_guid=data["guid"],
            title=data["title"],
            company_name=data["companyName"],
            description=html_to_text(data["description"]),
            is_expired=timestamp_is_expired(data["expiryDate"]),
            raw_data=data,
        )

    @classmethod
    def from_db_row(cls, data: dict[str, Any]) -> "Job":  # noqa: UP037
        data["db_id"] = data.pop("id")

        return cls(**data)

    def __str__(self) -> str:
        txt = f"[{self.source}] {self.title} at {self.company_name}"

        if self.is_expired:
            txt += " (expired)"

        return txt
