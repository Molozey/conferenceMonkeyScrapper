import json
from dataclasses import dataclass
import pandas as pd
from hashlib import md5
import uuid


@dataclass
class Event:
    model_config = {"arbitrary_types_allowed": True}

    event_info_source: str
    event_name: str

    event_location: str  # Could have geo type, but for simplify reasons i decide to use string
    event_date: pd.Timestamp

    event_description: str
    event_url: str

    event_meta_info: dict | str | None = None

    _event_uid: uuid.UUID = None

    def __post_init__(self):
        if self.event_meta_info is None:
            self.event_meta_info = {}
        self._event_uid = self.create_event_uid()
        self.event_meta_info = json.dumps(self.event_meta_info)

    def create_event_uid(self):
        encoded = str(
            {
                "event_info_source": self.event_info_source,
                "event_name": self.event_name,
                "event_location": self.event_location,
                "event_date": self.event_date,
            }
        ).encode("utf-8")
        return uuid.UUID(bytes=md5(encoded).digest(), version=4)

    @property
    def event_uid(self):
        return self._event_uid

    def __hash__(self):
        return hash(self.event_uid)
