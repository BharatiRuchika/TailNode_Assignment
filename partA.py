import requests
import mysql.connector

# Replace 'your_app_id' with the actual app ID obtained from the website
app_id = '65f1b6d518b4603c3de5ee40'

# Function to fetch users data from API
def fetch_users_data():
    url = 'https://dummyapi.io/data/v1/user'
    headers = {'app-id': app_id}
    response = requests.get(url, headers=headers)
    users_data = response.json()['data']
    return users_data

# Function to fetch posts data for a specific user
def fetch_user_posts(user_id):
    print('user_id',user_id)
    url = f'https://dummyapi.io/data/v1/user/{user_id}/post'
    headers = {'app-id': app_id}
    response = requests.get(url, headers=headers)
    print('response',response.json())
    # if response.status_code == 200:
    posts_data = response.json().get('data', [])
    print('posts_data',posts_data)
    return posts_data
    

# Function to store users data in the database
def store_users_data_in_db(users_data, cursor):
    for user in users_data:
        print('user' , user)
        cursor.execute('INSERT INTO users (id, title, firstName, lastName, picture) VALUES (%s, %s, %s, %s, %s)', (user['id'], user['title'], user['firstName'], user['lastName'],user['picture']))

# Function to store posts data in the database
def store_posts_data_in_db(user_id, posts_data, cursor):
    for post in posts_data:
        print('post',post)
        cursor.execute('INSERT INTO posts (id, user_id, text) VALUES (%s, %s, %s)', (post['id'], user_id, post['text']))

# Function to fetch users from the database
def fetch_users_from_db(cursor):
    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()
    return users

if __name__ == "__main__":
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ruchika@123',
        database='myDB'
    )
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id VARCHAR(255) PRIMARY KEY, title VARCHAR(255), firstName VARCHAR(255),lastName VARCHAR(255), picture VARCHAR(255))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                      (id VARCHAR(255) PRIMARY KEY, user_id VARCHAR(255), text TEXT)''')

    # Fetch users data and store in the database
    users_data = fetch_users_data()
    store_users_data_in_db(users_data, cursor)
    conn.commit()

    # Fetch users from the database and fetch their posts data
    users_from_db = fetch_users_from_db(cursor)
    for user_id in users_from_db:
        posts_data = fetch_user_posts(user_id[0])
        store_posts_data_in_db(user_id[0], posts_data, cursor)
        conn.commit()

    # Close connection
    cursor.close()
    conn.close()

    print("Data fetched and stored successfully!")
