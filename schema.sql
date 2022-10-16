CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT
);

CREATE TABLE user_movies (
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    name TEXT ,
    director TEXT,
    year INTEGER
);


CREATE TABLE ratings (
    movie_id INTEGER REFERENCES movies,
    user_id INTEGER,
    rating INTEGER,
    text TEXT,
    user_name TEXT
);

CREATE TABLE user_directors (
    user_id INTEGER REFERENCES users,
    director_id INTEGER REFERENCES directors
);

CREATE TABLE directors (
    id SERIAL PRIMARY KEY,
    name TEXT,
    birth_year INTEGER
);
