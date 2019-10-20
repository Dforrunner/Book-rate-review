ALTER TABLE books
  ADD COLUMN weights tsvector;
UPDATE books
SET weights = setweight(to_tsvector(isbn), 'A') ||
              setweight(to_tsvector(coalesce(title, '')), 'B') ||
              setweight(to_tsvector(coalesce(author, '')), 'C');
CREATE INDEX document_weights_idx
  ON books
  USING GIN (weights);

CREATE FUNCTION book_tsvector_trigger() RETURNS TRIGGER AS $$
BEGIN
  NEW.weights :=
     setweight(to_tsvector('english', coalesce(NEW.isbn, '')), 'A')
  || setweight(to_tsvector('english', coalesce(NEW.title, '')), 'B')
  || setweight(to_tsvector('english', coalesce(NEW.author, '')), 'C');
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON books FOR EACH ROW EXECUTE PROCEDURE book_tsvector_trigger();

-- Query the index
SELECT isbn, title, author, year
FROM books
where weights @@ to_tsquery('brook');