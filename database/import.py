import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Adds books that are in the books.csv into the database
def main():
    books = open("csv/books.csv")
    reader = csv.reader(books)
    next(reader)  # skip header
    count = 0

    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:isbn, :title, :author, :pyear)",
                   {"isbn": isbn, "title": title, "author": author, "pyear": year})
        print(f"{count} : {title} by {author}, year {year}, isbn: {isbn}")
        count += 1

    db.commit()


if __name__ == "__main__":
    main()
