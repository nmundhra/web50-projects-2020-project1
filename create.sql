CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL
);

CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  publishyear INTEGER NOT NULL
);

CREATE TABLE reviews (
  review_id SERIAL,
  rating SMALLINT NOT NULL,
  review VARCHAR,
  book_id INTEGER REFERENCES books(id),
  user_id INTEGER REFERENCES users(id),
  PRIMARY KEY(review_id, book_id, user_id)
);
