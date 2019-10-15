import requests

def get_reviews():
    res = requests.get("https://www.goodreads.com/book/isbn/",
                       params={"format": "json",
                               "key": "Un8q63xdxbWRHYNF97lyig",
                               "isbn": "0380795272",
                               })
    json_response = res.json()
    review_widget = json_response["reviews_widget"]
    print(review_widget)


def review_stats():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "Un8q63xdxbWRHYNF97lyig",
                               "isbns": "0380795272",
                               })
    json_response = res.json()
    isbn = json_response['books'][0]['isbn']
    isbn13 = json_response['books'][0]['isbn13']
    rating_count = json_response['books'][0]['work_ratings_count']
    review_count = json_response['books'][0]['work_reviews_count']
    avg_rating = json_response['books'][0]['average_rating']
    # print(json_response)
    print(isbn)
    print(isbn13)
    print(rating_count)
    print(review_count)
    print(avg_rating)

def main():
    review_stats()



if __name__ == '__main__':
    main()
