import csv
import sys
from flask import Flask
from models import Books
from config import Config
from ext import db
from third_party_api.book_cover_api import get_cover_image_url

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
'''
    Run this file to create the data and import the books from csv file into the database.
'''

def import_data():
    books = open("csv/books.csv")
    reader = csv.reader(books)
    next(reader)  # skip header
    count = 0
    for isbn, title, author, year in reader:
        img_url = get_cover_image_url(isbn)  # Gets the image url from APIs
        books = Books(isbn=isbn, title=title, author=author, year=year, image=img_url)
        db.session.add(books)

        # Prints visual progress. Just so that you know something is happening.
        count += 1
        sys.stdout.write('\r' + 'Imported: ' + str(count) + '/5000')

    db.session.commit()  # Commit changes to DB


def main():
    print("Creating database in progress...")
    db.create_all()
    print("Database created successfully!")
    print("\nImporting csv into database in progress...")
    #import_data()
    print("\nCompleted successfully!")


if __name__ == "__main__":
    with app.app_context():
        main()

