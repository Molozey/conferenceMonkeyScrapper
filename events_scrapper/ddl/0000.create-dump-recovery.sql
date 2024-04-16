create table if not exists scrapper.dump_recovery
(
    machine_id      integer,
    last_saved_url  text,
    last_saved_time timestamp
);

alter table scrapper.dump_recovery
    add constraint dump_recovery_pk
        primary key (machine_id, last_saved_time);

alter table scrapper.dump_recovery
    owner to postgres;

