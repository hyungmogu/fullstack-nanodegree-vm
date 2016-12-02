#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    conn = psycopg2.connect(database='forum')
    cur = conn.cursor()
    cur.execute('SELECT content,time FROM posts;')
    rows = cur.fetchall() 

    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in rows]
    posts.sort(key=lambda row: row['time'], reverse=True) #hey, how does this work?
    return posts

    conn.close()

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    conn = psycopg2.connect(database='forum')
    cur = conn.cursor()
    postDateAndTime = getPostDateAndTime()
    cur.execute('''INSERT INTO posts (content,time) VALUES (%s,%s);''',(content,postDateAndTime))

    conn.commit()
    conn.close()

def getPostDateAndTime():
  postDate = "-".join([ str(i) for i in time.localtime()[:3]])
  postTime = ":".join([ str(i) for i in time.localtime()[3:6]])
  postDateAndTime = " ".join([postDate,postTime])
  return postDateAndTime