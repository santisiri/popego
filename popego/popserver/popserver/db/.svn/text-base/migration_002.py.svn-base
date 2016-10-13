"""Create the revision table with a revision_id column."""

__docformat__ = "restructuredtext"


# I'm using a creative whitespace style that makes it readable both here
# and when printed.

migration = [
    ("""\
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

COMMENT ON SCHEMA public IS 'Standard public schema';

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE accounts (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    user_id integer,
    service_id integer
);

ALTER TABLE public.accounts OWNER TO popego;

CREATE SEQUENCE accounts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.accounts_id_seq OWNER TO popego;

ALTER SEQUENCE accounts_id_seq OWNED BY accounts.id;

CREATE TABLE groups (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);

ALTER TABLE public.groups OWNER TO popego;

CREATE SEQUENCE groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.groups_id_seq OWNER TO popego;

ALTER SEQUENCE groups_id_seq OWNED BY groups.id;

CREATE TABLE itemgroups (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    external_id character varying(255) NOT NULL,
    account_id integer
);

ALTER TABLE public.itemgroups OWNER TO popego;

CREATE SEQUENCE itemgroups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.itemgroups_id_seq OWNER TO popego;

ALTER SEQUENCE itemgroups_id_seq OWNED BY itemgroups.id;

CREATE TABLE itemgroups_items (
    itemgroups_id integer NOT NULL,
    user_items_id integer NOT NULL
);

ALTER TABLE public.itemgroups_items OWNER TO popego;

CREATE TABLE items (
    id integer NOT NULL,
    service_id integer NOT NULL,
    external_id character varying(2048) NOT NULL,
    title character varying(255),
    description character varying(512),
    row_type character varying(40)
);

ALTER TABLE public.items OWNER TO popego;

CREATE SEQUENCE items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.items_id_seq OWNER TO popego;

ALTER SEQUENCE items_id_seq OWNED BY items.id;

CREATE TABLE photos (
    item_id integer NOT NULL,
    url character varying(2048) NOT NULL,
    thumbnail_url character varying(2048)
);

ALTER TABLE public.photos OWNER TO popego;

CREATE TABLE roles (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);

ALTER TABLE public.roles OWNER TO popego;

CREATE SEQUENCE roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.roles_id_seq OWNER TO popego;

ALTER SEQUENCE roles_id_seq OWNED BY roles.id;

CREATE TABLE service_types (
    id integer NOT NULL,
    type character varying(64) NOT NULL,
    description character varying(255)
);

ALTER TABLE public.service_types OWNER TO popego;

CREATE SEQUENCE service_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.service_types_id_seq OWNER TO popego;

ALTER SEQUENCE service_types_id_seq OWNED BY service_types.id;

CREATE TABLE services (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    description character varying(256),
    url character varying(255) NOT NULL,
    agent character varying(255),
    type_id integer NOT NULL
);

ALTER TABLE public.services OWNER TO popego;

CREATE SEQUENCE services_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.services_id_seq OWNER TO popego;

ALTER SEQUENCE services_id_seq OWNED BY services.id;

CREATE TABLE user_items (
    id integer NOT NULL,
    creation_date timestamp without time zone,
    item_id integer
);

ALTER TABLE public.user_items OWNER TO popego;

CREATE SEQUENCE user_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.user_items_id_seq OWNER TO popego;

ALTER SEQUENCE user_items_id_seq OWNED BY user_items.id;

CREATE TABLE users (
    id integer NOT NULL,
    displayname character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    photo character varying(255),
    email character varying(50) NOT NULL,
    "shortBio" character varying(255),
    group_id integer
);

ALTER TABLE public.users OWNER TO popego;

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.users_id_seq OWNER TO popego;

ALTER SEQUENCE users_id_seq OWNED BY users.id;

CREATE TABLE users_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);

ALTER TABLE public.users_roles OWNER TO popego;

CREATE SEQUENCE users_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.users_roles_id_seq OWNER TO popego;

ALTER SEQUENCE users_roles_id_seq OWNED BY users_roles.id;

CREATE TABLE videos (
    item_id integer NOT NULL,
    "externalURL" character varying(2048) NOT NULL,
    "embedURL" character varying(2048) NOT NULL,
    author character varying(100)
);

ALTER TABLE public.videos OWNER TO popego;

CREATE TABLE videothumbnails (
    id integer NOT NULL,
    url character varying(255) NOT NULL,
    height integer,
    width integer,
    "time" character varying(20),
    video_item_id integer NOT NULL
);

ALTER TABLE public.videothumbnails OWNER TO popego;

CREATE SEQUENCE videothumbnails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE public.videothumbnails_id_seq OWNER TO popego;

ALTER SEQUENCE videothumbnails_id_seq OWNED BY videothumbnails.id;

ALTER TABLE accounts ALTER COLUMN id SET DEFAULT nextval('accounts_id_seq'::regclass);

ALTER TABLE groups ALTER COLUMN id SET DEFAULT nextval('groups_id_seq'::regclass);

ALTER TABLE itemgroups ALTER COLUMN id SET DEFAULT nextval('itemgroups_id_seq'::regclass);

ALTER TABLE items ALTER COLUMN id SET DEFAULT nextval('items_id_seq'::regclass);

ALTER TABLE roles ALTER COLUMN id SET DEFAULT nextval('roles_id_seq'::regclass);

ALTER TABLE service_types ALTER COLUMN id SET DEFAULT nextval('service_types_id_seq'::regclass);

ALTER TABLE services ALTER COLUMN id SET DEFAULT nextval('services_id_seq'::regclass);

ALTER TABLE user_items ALTER COLUMN id SET DEFAULT nextval('user_items_id_seq'::regclass);

ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

ALTER TABLE users_roles ALTER COLUMN id SET DEFAULT nextval('users_roles_id_seq'::regclass);

ALTER TABLE videothumbnails ALTER COLUMN id SET DEFAULT nextval('videothumbnails_id_seq'::regclass);

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_user_id_key UNIQUE (user_id, service_id);

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_name_key UNIQUE (name);

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);

ALTER TABLE ONLY itemgroups
    ADD CONSTRAINT itemgroups_external_id_key UNIQUE (external_id, account_id);

ALTER TABLE ONLY itemgroups_items
    ADD CONSTRAINT itemgroups_items_pkey PRIMARY KEY (itemgroups_id, user_items_id);

ALTER TABLE ONLY itemgroups
    ADD CONSTRAINT itemgroups_pkey PRIMARY KEY (id);

ALTER TABLE ONLY items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);

ALTER TABLE ONLY photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (item_id);

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);

ALTER TABLE ONLY service_types
    ADD CONSTRAINT service_types_pkey PRIMARY KEY (id);

ALTER TABLE ONLY service_types
    ADD CONSTRAINT service_types_type_key UNIQUE (type);

ALTER TABLE ONLY services
    ADD CONSTRAINT services_name_key UNIQUE (name);

ALTER TABLE ONLY services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);

ALTER TABLE ONLY user_items
    ADD CONSTRAINT user_items_pkey PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

ALTER TABLE ONLY users_roles
    ADD CONSTRAINT users_roles_pkey PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY videos
    ADD CONSTRAINT videos_pkey PRIMARY KEY (item_id);

ALTER TABLE ONLY videothumbnails
    ADD CONSTRAINT videothumbnails_pkey PRIMARY KEY (id);

CREATE INDEX ix_accounts_service_id ON accounts USING btree (service_id);

CREATE INDEX ix_accounts_user_id ON accounts USING btree (user_id);

CREATE INDEX ix_itemgroups_account_id ON itemgroups USING btree (account_id);

CREATE INDEX ix_items_service_id ON items USING btree (service_id);

CREATE INDEX ix_services_type_id ON services USING btree (type_id);

CREATE INDEX ix_user_items_item_id ON user_items USING btree (item_id);

CREATE INDEX ix_users_group_id ON users USING btree (group_id);

CREATE INDEX ix_users_roles_role_id ON users_roles USING btree (role_id);

CREATE INDEX ix_users_roles_user_id ON users_roles USING btree (user_id);

CREATE INDEX ix_videothumbnails_video_item_id ON videothumbnails USING btree (video_item_id);

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_service_id_fk FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE RESTRICT;

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY itemgroups
    ADD CONSTRAINT itemgroups_account_id_fk FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE;

ALTER TABLE ONLY itemgroups_items
    ADD CONSTRAINT itemgroups_items_fk FOREIGN KEY (itemgroups_id) REFERENCES itemgroups(id);

ALTER TABLE ONLY itemgroups_items
    ADD CONSTRAINT itemgroups_items_inverse_fk FOREIGN KEY (user_items_id) REFERENCES user_items(id);

ALTER TABLE ONLY items
    ADD CONSTRAINT items_service_id_fk FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE RESTRICT;

ALTER TABLE ONLY photos
    ADD CONSTRAINT photos_item_id_fkey FOREIGN KEY (item_id) REFERENCES items(id);

ALTER TABLE ONLY services
    ADD CONSTRAINT services_type_id_fk FOREIGN KEY (type_id) REFERENCES service_types(id) ON DELETE RESTRICT;

ALTER TABLE ONLY user_items
    ADD CONSTRAINT user_items_item_id_fk FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE RESTRICT;

ALTER TABLE ONLY users
    ADD CONSTRAINT users_group_id_fk FOREIGN KEY (group_id) REFERENCES groups(id);

ALTER TABLE ONLY users_roles
    ADD CONSTRAINT users_roles_role_id_fk FOREIGN KEY (role_id) REFERENCES roles(id);

ALTER TABLE ONLY users_roles
    ADD CONSTRAINT users_roles_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY videos
    ADD CONSTRAINT videos_item_id_fkey FOREIGN KEY (item_id) REFERENCES items(id);

ALTER TABLE ONLY videothumbnails
    ADD CONSTRAINT videothumbnails_video_item_id_fk FOREIGN KEY (video_item_id) REFERENCES videos(item_id);

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;

        """, 
     """\
DROP TABLE videothumbnails;
DROP TABLE videos;
DROP TABLE users_roles;
DROP TABLE roles;
DROP TABLE photos;
DROP TABLE itemgroups_items;
DROP TABLE itemgroups;
DROP TABLE user_items;
DROP TABLE items;
DROP TABLE accounts;
DROP TABLE services;
DROP TABLE service_types;
DROP TABLE users;
DROP TABLE groups;
     """),
]
