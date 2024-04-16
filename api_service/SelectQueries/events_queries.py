from fastapi import Query
from api_service.database import ENGINE
import pandas as pd


def construct_categorical_query(available_categories, default_is_none: bool = True):
    return Query(
        None if default_is_none else available_categories[0], enum=available_categories
    )


def get_available_event_info_source():
    q = f"""
    SELECT DISTINCT event_info_source
    FROM scrapper.scrapped_events
    """
    return list(pd.read_sql(q, ENGINE()).values.flatten())


if __name__ == "__main__":
    print(construct_categorical_query(get_available_event_info_source()))
