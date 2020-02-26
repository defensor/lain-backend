CREATE TABLE projects(
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE,
);

CREATE TABLE organizations(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    description TEXT,
    
    project_id INTEGER NOT NULL REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE buildings(
    id SERIAL PRIMARY KEY,
    addr VARCHAR(64) NOT NULL,
    name VARCHAR(32) NOT NULL,
    description TEXT
);

CREATE TABLE networks(
    id SERIAL PRIMARY KEY,
    addr VARCHAR(18) NOT NULL,
    name VARCHAR(32) NOT NULL,
    description TEXT
);

CREATE TABLE hosts(
    id SERIAL PRIMARY KEY,
    addr VARCHAR(15) NOT NULL,
    os VARCHAR(32),
    description TEXT

    network_id INTEGER NOT NULL REFERENCES networks (id) ON DELETE CASCADE
);

CREATE TABLE domains(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT,

    type_id INTEGER REFERENCES domain_types (id) ON DELETE SET NULL
);

CREATE TABLE services(
    id SERIAL PRIMARY KEY,
    port INTEGER NOT NULL,
    name VARCHAR(64) NOT NULL,
    version VARCHAR(64),
    description TEXT
);

CREATE TABLE domain_types(
    id SERIAL PRIMARY KEY,
    name VARCHAR(8) NOT NULL UNIQUE
);

CREATE TABLE protocols(
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE credentials(
    id SERIAL PRIMARY KEY,
    login VARCHAR(64),
    password VARCHAR(128),
    key VARCHAR(512), 
    description TEXT
);

CREATE TABLE vulnerabilities(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    solution TEXT,
    description TEXT
);

CREATE TABLE peoples(
    id SERIAL PRIMARY KEY,
    firtsname VARCHAR(16),
    surname VARCHAR(16),
    patronymic VARCHAR(16),
    position VARCHAR(32),
    description TEXT
);

CREATE TABLE contacts(
    id SERIAL PRIMARY KEY,
    value VARCHAR(32) NOT NULL,
    description TEXT,

    type_id INTEGER REFERENCES contact_types (id) ON DELETE SET NULL
);

CREATE TABLE contact_types(
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE organizations_networks(
    organization_id INTEGER NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    network_id INTEGER NOT NULL REFERENCES networks (id) ON DELETE CASCADE
);

CREATE TABLE organizations_buildings(
    organization_id INTEGER NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    building_id INTEGER NOT NULL REFERENCES buildings (id) ON DELETE CASCADE
);

CREATE TABLE hosts_domains(
    host_id INTEGER NOT NULL REFERENCES hosts (id) ON DELETE CASCADE
    domain_id INTEGER NOT NULL REFERENCES domains (id) ON DELETE CASCADE
);

CREATE TABLE organizations_peoples(
    organization_id INTEGER NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    people_id INTEGER NOT NULL REFERENCES peoples (id) ON DELETE CASCADE
);

CREATE TABLE peoples_vulnerabilities(
    people_id INTEGER NOT NULL REFERENCES peoples (id) ON DELETE CASCADE
    vulnerability_id INTEGER NOT NULL REFERENCES vulnerabilities (id) ON DELETE CASCADE
);

CREATE TABLE networks_vulnerabilities(
    network_id INTEGER NOT NULL REFERENCES networks (id) ON DELETE CASCADE
    vulnerability_id INTEGER NOT NULL REFERENCES vulnerabilities (id) ON DELETE CASCADE
);

CREATE TABLE hosts_vulnerabilities(
    host_id INTEGER NOT NULL REFERENCES hosts (id) ON DELETE CASCADE
    vulnerability_id INTEGER NOT NULL REFERENCES vulnerabilities (id) ON DELETE CASCADE
);

CREATE TABLE organizations_contacts(
    organization_id INTEGER NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    contact_id INTEGER NOT NULL REFERENCES contacts (id) ON DELETE CASCADE
);

CREATE TABLE peoples_contacts(
    people_id INTEGER NOT NULL REFERENCES peoples (id) ON DELETE CASCADE
    contact_id INTEGER NOT NULL REFERENCES contacts (id) ON DELETE CASCADE
);

CREATE TABLE services_vulnerabilities(
    service_id INTEGER NOT NULL REFERENCES services (id) ON DELETE CASCADE,
    vulnerability_id INTEGER NOT NULL REFERENCES vulnerabilities (id) ON DELETE CASCADE
);

CREATE TABLE services_credentials(
    service_id INTEGER NOT NULL REFERENCES services (id) ON DELETE CASCADE,
    credential_id INTEGER NOT NULL REFERENCES credentials (id) ON DELETE CASCADE
);

CREATE TABLE services_protocols(
    service_id INTEGER NOT NULL REFERENCES services (id) ON DELETE CASCADE,
    protocol_id INTEGER NOT NULL REFERENCES protocols (id) ON DELETE CASCADE
);