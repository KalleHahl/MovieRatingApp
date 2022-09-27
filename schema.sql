CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    director TEXT,
    year INTEGER
);