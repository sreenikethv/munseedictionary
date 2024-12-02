#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Sreeniketh Vogoti
#-----------------------------------------------------------------------

"""Helper module mediating requests to the SQL database."""
import sys
import contextlib
import sqlite3
import re


_DATABASE_URL = 'file:dictionary.sqlite?mode=ro' # url to test working db

#-----------------------------------------------------------------------
# Function to get the details of a word entry from the database
def get_entry(request_json):
    """function that returns a database retrieval for a single course"""
    try:
        with sqlite3.connect(_DATABASE_URL,
            isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                entry = request_json['entry']
                # Select data on course if it is valid
                stmt_str = """
                SELECT * 
                FROM words
                """

                # List to hold query parameters
                params = []
                
                # Add conditions to SQL if parameters are provided
                if entry:
                    stmt_str += " WHERE entry LIKE ? OR definition LIKE ?"
                    params.extend([f"%{entry}%", f"%{entry}%"])


                semantic_category = request_json['semantic_category']

                if semantic_category:
                    if 'WHERE' in stmt_str:
                        stmt_str += " AND semantic_category LIKE ?"
                    else:
                        stmt_str += " WHERE semantic_category LIKE ?"
                    params.append(f"%{semantic_category}%")     

                cursor.execute(stmt_str, params)
                table = cursor.fetchall()

                # error handling
                request_handled_bool = True
                for row in table:
                    if None in row:
                        class_dict = f"""'{entry}' not found"""
                        request_handled_bool = False
                        break

                else:
                    # build response json
                    entries = []
                    for row in table:
                        new_dict = {'entry':render_main_spelling(row[0]),
                        'underlying':row[1],
                        'pos':row[2], 'definition':row[3],
                        'semantic_category':row[4], 'etymology':row[5],
                        'related':row[6], 'examples':row[7],
                        'tags':row[8], 'notes':row[9], 'source':row[10]}
                        entries.append(new_dict)
                output = [request_handled_bool, entries]
                return output

    except Exception as ex:
        print(f'database.py: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------
def render_main_spelling(word):
    output = word.split(';')[0]
    #remove bracketed text (e.g. wte[e]hiim -> wtehiim)
    output = re.sub('\[.*?\]', '', output)
    return output
#-----------------------------------------------------------------------
def get_all_categories(request_json):
    try:
        with sqlite3.connect(_DATABASE_URL,
            isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                entry = request_json['entry']
                # Select data on course if it is valid
                course_str = """
                SELECT DISTINCT semantic_category
                FROM words
                WHERE semantic_category IS NOT NULL
                """
                cursor.execute(course_str)
                table = cursor.fetchall()
                
                # error handling
                request_handled_bool = True
                for row in table:
                    if None in row:
                        class_dict = f"""'{entry}' not found"""
                        request_handled_bool = False
                        break

                else:
                    # build response json
                    entries = []
                    for row in table:
                        entries.append(row[0])
                    entries.sort()
                output = [request_handled_bool, entries]
                return output

    except Exception as ex:
        print(f'database.py: {ex}', file=sys.stderr)
        sys.exit(1)
#-----------------------------------------------------------------------

if __name__ == '__main__':
    _test()
