import os
import requests
import urllib3

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
        gr_book_id = json_response['books'][0]['id']
        book_isbn = json_response['books'][0]['isbn']
        book_isbn13 = json_response['books'][0]['isbn13']
        rating_count = json_response['books'][0]['work_ratings_count']
        review_count = json_response['books'][0]['work_reviews_count']
        avg_rating = json_response['books'][0]['average_rating']


    except Exception:
        print("Error getting review stats")
    print(json_response)
    print(gr_book_id)
    print(book_isbn)
    print(book_isbn13)
    print(rating_count)
    print(review_count)
    print(avg_rating)


def create_review(id):
    post_review = "Error posting review."
    try:
        res = requests.get("https://www.goodreads.com/review.xml",
                           params={"book_id": id,
                                    "key": os.getenv("GoodReads_API_KEY"),
                                   })
        print(os.getenv("GoodReads_API_KEY"))
        print(f"request status code: {res.status_code}")

    except Exception:
        print("Error getting review widget")


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
        print(review_widget)
    except Exception:
        print("Error getting review widget")

    return review_widget


def main():
    print("testing zone")
    #get_review_stats("0380795272")
    get_reviews('0380795272')
    #create_review("92918")


if __name__ == '__main__':
    main()
