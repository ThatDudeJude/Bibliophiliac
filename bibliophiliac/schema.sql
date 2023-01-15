CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    name VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY, 
    isbn VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year VARCHAR NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, 
    rating INTEGER NOT NULL,
    opinion VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name_id INTEGER,
    book_isbn VARCHAR NOT NULL,
    FOREIGN KEY (name_id) REFERENCES users (id),
    FOREIGN KEY (book_isbn) REFERENCES books (isbn)
);
