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

CREATE TABLE networks (
    id serial PRIMARY KEY,
    addr cidr NOT NULL,
    name varchar(32) NOT NULL,
    description varchar(512)
);

CREATE TABLE hosts (
    id serial PRIMARY KEY,
    addr inet NOT NULL,
    os varchar(32),
    description varchar(512),
    network_id integer NOT NULL REFERENCES networks (id) ON DELETE CASCADE
);

CREATE TABLE domain_types (
    id serial PRIMARY KEY,
    name varchar(8) NOT NULL UNIQUE
);

CREATE TABLE domains (
    id serial PRIMARY KEY,
    name varchar(64) NOT NULL,
    description varchar(512),
    type_id integer REFERENCES domain_types (id) ON DELETE SET NULL
);

CREATE TABLE services (
    id serial PRIMARY KEY,
    port integer NOT NULL,
    name varchar(64) NOT NULL,
    version varchar(64),
    description varchar(512),
    host_id integer REFERENCES hosts (id) ON DELETE CASCADE
);

CREATE TABLE protocols (
    id serial PRIMARY KEY,
    name varchar(32) NOT NULL UNIQUE
);

CREATE TABLE organizations_networks (
    organization_id integer NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    network_id integer NOT NULL REFERENCES networks (id) ON DELETE CASCADE
);

CREATE TABLE hosts_domains (
    host_id integer NOT NULL REFERENCES hosts (id) ON DELETE CASCADE,
    domain_id integer NOT NULL REFERENCES domains (id) ON DELETE CASCADE
);

CREATE TABLE services_protocols (
    service_id integer NOT NULL REFERENCES services (id) ON DELETE CASCADE,
    protocol_id integer NOT NULL REFERENCES protocols (id) ON DELETE CASCADE
);
