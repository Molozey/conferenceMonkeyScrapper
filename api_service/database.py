from __future__ import annotations
from api_service.logs import create_logger
from sqlalchemy import create_engine
from pandas import DataFrame, Timestamp, read_sql
from dataclasses import asdict
from sqlalchemy.dialects.postgresql import insert
import os

HOST = os.getenv("NET_NAME", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PWD = os.getenv("DB_PWD", "postgres")

LOGGER = create_logger(__name__)


def postgres_upsert(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_update(
        constraint=f"{table.table.name}_pk",
        set_={c.key: c for c in insert_statement.excluded},
    )
    conn.execute(upsert_statement)


def insert_or_update_events(events: list["Event"]):
    lists_for_df = []
    # FIXME: need it for debug purposes
    for event in events:
        try:
            lists_for_df.append(asdict(event))
        except Exception as e:
            # print(type(event))
            # print(event)
            # print(e)
            raise e
    events_df = DataFrame(lists_for_df)
    events_df.rename(columns={"_event_uid": "event_uuid"}, inplace=True)
    events_df = events_df.assign(updated_at=Timestamp.utcnow())
    # FIXME: hardcoded path
    events_df.to_sql(
        name="scrapped_events",
        con=ENGINE(),
        schema="scrapper",
        if_exists="append",
        index=False,
        method=postgres_upsert,
    )


def select_last_scrapped_url(machine_id: int) -> DataFrame:
    q = f"""
    SELECT * FROM scrapper.dump_recovery
    WHERE machine_id = {machine_id}
    ORDER BY last_saved_time DESC
    LIMIT 1
    """
    return read_sql(q, ENGINE())


def insert_last_scrapped_url(df: DataFrame):
    LOGGER.info(f"Setting new last id {df}")
    df = df.assign(last_saved_time=Timestamp.utcnow())
    # FIXME: hardcoded path
    df.to_sql(
        name="dump_recovery",
        con=ENGINE(),
        schema="scrapper",
        if_exists="append",
        index=False,
        method=postgres_upsert,
    )


ENGINE = lambda: create_engine(
    f"postgresql://{DB_USER}:{DB_PWD}@{HOST}:{DB_PORT}/{DB_NAME}"
)


if __name__ == "__main__":
    pass
