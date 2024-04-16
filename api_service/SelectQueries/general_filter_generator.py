import pandas as pd
from typing import Literal, Union
from dataclasses import dataclass

compare_operations = Literal["<", ">", "=", "!="]


@dataclass
class Filter:
    filter_column: str
    filter_value: Union[str, pd.Timestamp]
    filter_operation: Literal["<", ">", "=", "!="]

    def create_filter(self) -> str:
        if self.filter_value == "NULL":
            if self.filter_operation == "=":
                return f"{self.filter_column} is {self.filter_value}"
            elif self.filter_operation == "!=":
                return f"{self.filter_column} is not {self.filter_value}"
            else:
                raise KeyError("Unavailable sign for NULL check")
        if isinstance(self.filter_value, str):
            return f"{self.filter_column} {self.filter_operation} '{self.filter_value}'"
        elif isinstance(self.filter_value, pd.Timestamp):
            return f"{self.filter_column} {self.filter_operation} '{self.filter_value.isoformat()}'"


def general_filter_scrapped_events_generator(
    filters: list[Filter],
    columns_list: list[str] = None,
    page_number: int = None,
    page_size: int = None,
    return_count: bool = False,
):
    """
    Params should have same name like at table
    """
    header_part = "SELECT * FROM scrapper.scrapped_events"
    offset_limit_request = ""

    if page_size and page_number:
        offset_limit_request = f"""
        OFFSET {int(page_number - 1) * page_size if page_number != 0 else 0}
        LIMIT {page_size}
        """
    if columns_list:
        header_part = f"SELECT {', '.join(columns_list)} FROM scrapper.scrapped_events"
    if return_count:
        header_part = f"SELECT COUNT(*) FROM scrapper.scrapped_events"

    where_part = ""
    if filters:
        where_part += f"WHERE {filters[0].create_filter()}"
        for _where_cond in filters[1:]:
            where_part += f"\nAND {_where_cond.create_filter()}"

    return header_part + "\n" + where_part + offset_limit_request


FILTERS = [
    Filter(
        filter_column="event_info_source", filter_value="NULL", filter_operation="!="
    ),
    Filter(filter_column="event_name", filter_value="NULL", filter_operation="!="),
    Filter(filter_column="event_location", filter_value="NULL", filter_operation="!="),
    Filter(
        filter_column="event_date",
        filter_value=pd.Timestamp("2024-01-01"),
        filter_operation=">",
    ),
    Filter(
        filter_column="updated_at",
        filter_value=pd.Timestamp("2024-01-01"),
        filter_operation=">",
    ),
]

if __name__ == "__main__":
    print(
        general_filter_scrapped_events_generator(FILTERS, page_number=1, page_size=20)
    )
