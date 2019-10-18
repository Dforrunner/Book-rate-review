import os
import requests
from PIL import Image
from io import BytesIO

'''
    First tries to get book cover image url from LibraryThing API.
    If the image size is 1x1 it means the book cover isn't available in the LibraryThing API.
    In such case it tries to check is it exists in the Open Library Covers API:
    Used in home.html, book_page.html, etc to display book cover images.
    
    Link to LibraryThing cover API: https://blog.librarything.com/main/2008/08/a-million-free-covers-from-librarything/
    Link to Open Covers API Docs: https://openlibrary.org/dev/docs/api/covers
'''


def get_image_size(url):
    try:
        data = requests.get(url).content
        img_data = Image.open(BytesIO(data))
    except Exception:
        print("Error getting image size")

    return img_data.size


def get_cover_image_url(isbn):
    goodreads_img_url = f"http://covers.librarything.com/devkey/{os.getenv('LibraryThing_API_KEY')}/large/isbn/{isbn}"
    width, height = get_image_size(goodreads_img_url)
    if width > 1 and height > 1:
        return goodreads_img_url
    else:
        openlib_img_url = f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        return openlib_img_url
