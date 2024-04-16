create table if not exists scrapper.scrapped_events
(
    event_uuid        text
        constraint scrapped_events_pk
            primary key,
    event_info_source text,
    event_name        text,
    event_location    text,
    event_date        timestamp,
    event_description text,
    event_meta_info   jsonb,
    event_url         text,
    updated_at        timestamp
);

