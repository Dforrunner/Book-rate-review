Book Rate and Review App.
This is simple project I'm working on to learn Flask. 

Current functionalities of the site are: 
 - Search books by title, author, isbn, and year
 - User accounts:
    - Sing in
    - Sign up
    - Add books to bookshelf
    - Remove books from bookshelf
    - Change username
    - Change password 
    - Delete account
    
Rate and review functionalities aren't implemented by me yet, but you can still leave a rating and a review via
Goodreads API. I am using Goodreads Api for all the book reviews and stats. 

For book cover images I am getting them from the following APIs:   
    - Link to LibraryThing cover API: https://blog.librarything.com/main/2008/08/a-million-free-covers-from-librarything/
    - Link to Open Covers API Docs: https://openlibrary.org/dev/docs/api/covers 

I will be moving onto another project at this point, but will be revisiting this one to implement tests and apply some
of my new knowledge that I hope to gain from the future projects. 

Feel free to fork this project and play around with it yourself.
To get this project up and running on your machine...
- You'll need everything listed in the requirements.txt other than pytest unless if you wish to implement that yourself.
  Use Pip to download them. 
- Set the environment variables that are in the config.py (You'll see TODO's for those that you need to set).
  You'll get errors if your environment variables aren't set.
  There are 2 environment variables you'll need to set that are not in the config file. They are API keys used to gain access 
  to the Goodreads API and book cover image API's.
  There are the 2 additional environment variables you'll need to set:
      1. LibraryThing_API_KEY  (get key from https://blog.librarything.com/main/2008/08/a-million-free-covers-from-librarything/)
      2. GoodReads_API_KEY     (get key from https://www.goodreads.com/api/)
- Once you've set your environment variables run create_db.py located in the db directory.
- At this point you should be good to run the flask app.
