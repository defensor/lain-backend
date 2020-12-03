CREATE TABLE projects (
    id serial PRIMARY KEY,
    name varchar(128) NOT NULL UNIQUE
);

CREATE TABLE organizations (
    id serial PRIMARY KEY,
    name varchar(64) NOT NULL UNIQUE,
    description varchar(512),
    project_id integer NOT NULL REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE hosts (
    id serial PRIMARY KEY,
    addr inet NOT NULL,
    os text,
    description varchar(512)
);

CREATE TABLE domains (
    id serial PRIMARY KEY,
    name varchar(64) NOT NULL,
    description varchar(512),
    record varchar(32) NOT NULL
);

CREATE TABLE services (
    id serial PRIMARY KEY,
    port integer NOT NULL,
    state varchar(16) NOT NULL,
    proto3 varchar(8) NOT NULL,
    proto7 varchar(32),
    version varchar(64),
    description varchar(512),
    host_id integer REFERENCES hosts (id) ON DELETE CASCADE
);

CREATE TABLE organizations_hosts (
    organization_id integer NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    host_id integer NOT NULL REFERENCES hosts (id) ON DELETE CASCADE
);

CREATE TABLE hosts_domains (
    host_id integer NOT NULL REFERENCES hosts (id) ON DELETE CASCADE,
    domain_id integer NOT NULL REFERENCES domains (id) ON DELETE CASCADE
);
