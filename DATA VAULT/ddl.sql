-- Создаем БД PostgreSQL

    CREATE DATABASE posts
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Создаем схемы для слоев STG и DDS

    CREATE SCHEMA stg
    AUTHORIZATION postgres;

    CREATE SCHEMA dds
    AUTHORIZATION postgres;

 -- Создаем таблицы с необходимыми сущностями 
 -- https://drawsql.app/teams/home-175/diagrams/post-diagram

    CREATE TABLE stg.post
    (
    user_id bigint,
    id bigint,
    title text,
    body text,
    load_dt timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id, load_dt)
    );
    ALTER TABLE IF EXISTS stg.post
    OWNER to postgres;


    CREATE TABLE dds.hub_post
    (
        post_hash_key text,
        load_dt timestamp DEFAULT current_timestamp,
        PRIMARY KEY (post_hash_key, load_dt)
    );

    ALTER TABLE IF EXISTS dds.hub_post
        OWNER to postgres;

    CREATE TABLE dds.lnk_post_user
    (
        post_hash_key text,
        user_hash_key text,
        load_dt timestamp DEFAULT current_timestamp,
        PRIMARY KEY (post_hash_key, user_hash_key, load_dt)
    );

    ALTER TABLE IF EXISTS dds.lnk_post_user
        OWNER to postgres;

    CREATE TABLE dds.hub_user
    (
        user_hash_key text,
        load_dt timestamp DEFAULT current_timestamp,
        PRIMARY KEY (user_hash_key, load_dt)
    );

    ALTER TABLE IF EXISTS dds.hub_user
        OWNER to postgres;

    CREATE TABLE dds.sat_post
    (
        post_hash_key text,
        title text,
        body text,
        load_dt timestamp DEFAULT current_timestamp,
        PRIMARY KEY (post_hash_key, load_dt)
    );

    ALTER TABLE IF EXISTS dds.sat_post
        OWNER to postgres;
