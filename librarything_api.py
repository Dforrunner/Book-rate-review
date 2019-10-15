import requests
import os

'''
    Gets book cover image url from LibraryThing API.
    Used in home.html, book_page.html, etc to display book cover images.
'''
def get_cover_image_url(isbn, size):
    return f"http://covers.librarything.com/devkey/{os.getenv('LibraryThing_API_KEY')}/{size}/isbn/{isbn}"
