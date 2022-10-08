CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    director TEXT,
    year INTEGER,
    user_id INTEGER
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    movie_name TEXT,
    user_id INTEGER,
    rating INTEGER,
    text TEXT,
    user_name TEXT
);

CREATE TABLE directors (
    id SERIAL PRIMARY KEY,
    name TEXT,
    birth_year INTEGER,
    user_id INTEGER
);