from bs4 import BeautifulSoup
import urllib
from urllib import request
import urllib.request as ur
import sqlite3
import mysql.connector


# Getting url for website 
urlinput = 'http://books.toscrape.com/'
print(" This is the website link that you entered", urlinput)

# For extracting specific tags from webpage
def getTags(tag):
  s = ur.urlopen(urlinput)
  soup = BeautifulSoup(s.read(),features="lxml")
  
  return soup.select(tag)


def scrape_books(url):
    tags = getTags('.product_pod')
    data = []
    for tag in tags:
        title = tag.h3.a['title']
        price = tag.find('p', class_='price_color').text
        availability = 'In stock' if 'instock' in tag.find('p', class_='instock availability').text.lower() else 'Out of stock'
        rating = ' '.join(tag.find('p', class_='star-rating')['class'][-1].split())
        data.append((title, price, availability, rating))
    return data


# function to store all data inside the database
def store_books_in_db(books_data):
    print('books_data',books_data)
    try:
        print("im in try block")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ruchika@123',
            database='Books'
        )
        c = conn.cursor()
    
        # query to create table books in mysql
        c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INT AUTO_INCREMENT PRIMARY KEY, 
             title VARCHAR(255), 
             price VARCHAR(255), 
             availability TEXT, 
             rating VARCHAR(255))''')
        
        # insert data inside the table books
        c.executemany('INSERT INTO books ( title, price, availability, rating ) VALUES (%s, %s, %s, %s)', books_data)
        conn.commit()
       
    except mysql.connector.Error as e:
        print("MySQL error:", e)
    finally:
        print("Data fetched and stored successfully!")
        conn.close()
    


#------------- Main ---------------#
if __name__ == '__main__':
    
    # getting tags having class product_pod
    
        # print(tag) # display tags 
        # print(tag.contents) # display contents of the tags
    

    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    all_books = []
    for page_num in range(1, 51):  # Scraping 50 pages
        url = base_url.format(page_num)
        books_data = scrape_books(url)
        all_books.extend(books_data)

    store_books_in_db(all_books)



