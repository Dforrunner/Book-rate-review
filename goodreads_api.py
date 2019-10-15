import requests
import os


'''
    Get Good Reads Review Widget. 
    Returns iframe of the widget.
    Used in book_page.html to display reviews. 
'''
def get_reviews(isbn):
    try:
        res = requests.get("https://www.goodreads.com/book/isbn/",
                           params={"format": "json",
                                   "key": os.getenv("GoodReads_API_KEY"),
                                   "isbn": isbn,
                                   })
        json_response = res.json()
        review_widget = json_response["reviews_widget"]

    except Exception:
        print("Error getting review widget")

    return review_widget


'''
    Gets review stats from GoodReads API.
    Used in book_page.html to show book review stats
'''
def get_review_stats(isbn):
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": os.getenv("GoodReads_API_KEY"),
                                   "isbns": isbn,
                                   })
        json_response = res.json()
        book_isbn = json_response['books'][0]['isbn']
        book_isbn13 = json_response['books'][0]['isbn13']
        rating_count = json_response['books'][0]['work_ratings_count']
        review_count = json_response['books'][0]['work_reviews_count']
        avg_rating = json_response['books'][0]['average_rating']

    except Exception:
        print("Error getting review stats")

    return {
            "isbn": book_isbn,
            "isbn13": book_isbn13,
            "rating_count": rating_count,
            "review_count": review_count,
            "avg_rating": avg_rating
            }
