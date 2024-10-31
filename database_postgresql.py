#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Sreeniketh Vogoti
#-----------------------------------------------------------------------

"""Helper module mediating requests to the SQL database."""
import flask
import psycopg2
from psycopg2.extras import RealDictCursor


app = flask.Flask(__name__)

# Database connection settings
DB_SETTINGS = {
    "dbname": "dictionary",
    "user": "your_username",  # replace with actual username
    "password": "your_password",  # replace with actual password
    "host": "localhost",
    "port": 5560
}

# Function to connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(**DB_SETTINGS)

# Function to get the details of a word entry from the database
def get_entry(request_json):
    entry = request_json['entry']

    conn = connect_db()
    # Returns rows as dictionaries
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT entry, underlying, pos, definition, semantic_category,
            etymology, related, examples, tags, notes, source 
        FROM entries
        WHERE entry = %s
    """
    cursor.execute(query, (entry,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        # result is in dictionary format and can be returned as json
        return result
    return None

def handle_request(request_json):
    return request_json
#-----------------------------------------------------------------------
'''
def _test():
    course_list = handle_request(8291)
    course = course_list[1]
    print(course['classid'])
'''

if __name__ == '__main__':
    app.run(debug=True)
