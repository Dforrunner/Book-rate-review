import os
import requests
from PIL import Image
from io import BytesIO

'''
    First tries to get book cover image url from Open Covers API.
    If the image size is 1x1 it means the book cover isn't available in the Open Covers API.
    In such case it tries to check is it exists in the LibraryThing Covers API:
    Used in home.html, book_page.html, etc to display book cover images.
    
    Link to LibraryThing cover API: https://blog.librarything.com/main/2008/08/a-million-free-covers-from-librarything/
    Link to Open Covers API Docs: https://openlibrary.org/dev/docs/api/covers
'''


def get_image_size(url):
    w, h = 0, 0
    try:
        req = requests.get(url).content
        im = Image.open(BytesIO(req))
        w, h = im.size
    except Exception:
        print("Error getting image size")
    return w, h


def get_cover_image_url(isbn):
    openlib_img_url = f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
    width, height = get_image_size(openlib_img_url)
    if width > 1 and height > 1:
        return openlib_img_url
    else:
        goodreads_img_url = f"http://covers.librarything.com/devkey/{os.getenv('LibraryThing_API_KEY')}/large/isbn/{isbn}"
        width2, height2 = get_image_size(goodreads_img_url)
        if width2 > 1 and height2 > 1:
            return goodreads_img_url
        else:
            # If cover image is not found in either api, then add placeholder image
            placeholder_url = "https://www.nilfiskcfm.com/wp-content/uploads/2016/12/placeholder.png"
            return placeholder_url
