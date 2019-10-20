ALTER TABLE books
  ADD COLUMN document tsvector;
UPDATE books
SET document = setweight(to_tsvector(isbn), 'A') ||
              setweight(to_tsvector(coalesce(title, '')), 'B') ||
              setweight(to_tsvector(coalesce(author, '')), 'C')||
              setweight(to_tsvector(CAST(year AS VARCHAR)), 'D');
CREATE INDEX document_weights_idx
  ON books
  USING GIN (document);

CREATE FUNCTION book_tsvector_trigger() RETURNS TRIGGER AS $$
BEGIN
  NEW.document :=
     setweight(to_tsvector('english', coalesce(NEW.isbn, '')), 'A')
  || setweight(to_tsvector('english', coalesce(NEW.title, '')), 'B')
  || setweight(to_tsvector('english', coalesce(NEW.author, '')), 'C')
  || setweight(to_tsvector('english', coalesce(NEW.year, '')), 'D');
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON books FOR EACH ROW EXECUTE PROCEDURE book_tsvector_trigger();

-- Query advanced search operators: and(&), or(|), not(!), proximity(<->) note: <3> means 3 words apart
SELECT isbn, title, author, year
FROM books
where document @@ to_tsquery('brook&2006');