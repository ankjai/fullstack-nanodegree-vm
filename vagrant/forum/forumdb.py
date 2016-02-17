#
# Database access functions for the web forum.
# 

import bleach
import psycopg2

## Database connection
conn = psycopg2.connect("dbname=forum")

# Open a cursor to perform database operations
cur = conn.cursor()


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    # select stmn
    sql = "SELECT content, time FROM posts ORDER BY time DESC;"

    # Query the database and obtain data as Python objects
    cur.execute(sql)

    # fetch all
    resultSet = cur.fetchall()

    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in resultSet]
    # no need to sort as result set is sorted by time
    # also getting a sorted result is much more efficient than getting unsorted result
    # and then sorting in code (imagine when resultSet is huge)
    # posts.sort(key=lambda row: row['time'], reverse=True)
    return posts


## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    # get time to timestamp the post
    # t = time.strftime('%c', time.localtime())

    # insert statement
    sql = "INSERT INTO posts(content) VALUES(%s);"

    # use bleach to
    # escapes or strips markup and attributes
    content = bleach.clean(content)

    # exe insert statement
    # use tuple to avoid db injection issues
    cur.execute(sql, (content,))

    # Make the changes to the database persistent
    conn.commit()
