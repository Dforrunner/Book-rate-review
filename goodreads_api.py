import requests
import os


'''
    Get Good Reads Review Widget. 
    Returns iframe of the widget.
    Used in book_page.html to display reviews. 
'''
def get_reviews(isbn):
    review_widget = "Error getting reviews."
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
    The method below basically converts a rating out off 5 into percent. 
    Used to set the width of the star rating css. 100% rate  = 125% five star
'''
def convert_rating_to_percent(num, size):
    if size == "small":
        return str((num/4)*100) + '%'
    elif size == "large":
        return str((num/2.4)*100) + '%'


'''
    Gets review stats from GoodReads API.
    Used in book_page.html to show book review stats
'''
def get_review_stats(isbn):
    book_isbn = "Data not found."
    book_isbn13 = "Data not found."
    rating_count = "Data not found."
    review_count = "Data not found."
    percent_avg_rating = "0%"

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

        # Used to color in the star ratings
        percent_avg_rating = convert_rating_to_percent(float(avg_rating), "large")
    except Exception:
        print("Error getting review stats")

    return {
            "isbn": book_isbn,
            "isbn13": book_isbn13,
            "rating_count": rating_count,
            "review_count": review_count,
            "percent_avg_rating": percent_avg_rating
            }


def get_avg_rating(isbn):
    percent_avg_rating = "0%"
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": os.getenv("GoodReads_API_KEY"),
                                   "isbns": isbn,
                                   })
        json_response = res.json()
        avg_rating = json_response['books'][0]['average_rating']

        # Used to color in the star ratings
        percent_avg_rating = convert_rating_to_percent(float(avg_rating), "small")
    except Exception:
        print("Error getting avg rating")

    return percent_avg_rating
