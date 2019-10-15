-- Creating the tables and relations (Many-to-Many)
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL
);

CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL,
    year INTEGER
);

CREATE TABLE rates_reviews(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    reviews VARCHAR(1500),
    rating NUMERIC(2)
);