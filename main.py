#!/usr/bin/env python
import psycopg2

"""
The connection is opened at the start of the program and closed in the end.

The same connection is used throughout the program
"""

# Connect to the database and create a cursor. 
# Cursor is closed before the program finishes.
db = psycopg2.connect("dbname=news")
cur = db.cursor()

def topArticles(topmost=3):
    """ Returns the topmost viewed articles from the database. 

        Return value is a tuple with the columns and the result object.
    """
    query = """
    SELECT title, count(log.id)
    FROM log
    JOIN articles
    ON log.path = concat('/article/', slug)
    GROUP BY title
    ORDER BY count DESC
    LIMIT %s ;
    """
    cur.execute(query, (topmost,) )
    colnames = [desc[0] for desc in cur.description]
    return (colnames, cur.fetchall())

def topAuthors(topmost=10):
    """ Returns the topmost viewed authors from the database.

        Return value is a tuple with the columns and the result object.
        Most viewed author is computed by comparing the sum of the views of
        each of the author's articles
    """
    query = """
     SELECT authors.name, count(log.id)
     AS views
     FROM authors
     JOIN articles
     ON authors.id = articles.author
     JOIN log
     ON concat('/article/', articles.slug) = log.path
     GROUP BY authors.name
     ORDER BY views DESC
     LIMIT %s ;
    """
    cur.execute(query, (topmost,) )
    colnames = [desc[0] for desc in cur.description]
    return (colnames, cur.fetchall())

def topErrorsPerDay(topmost_percent = 1):
    """
    Returns the days with at least topmost_percent responses as errors.

    The returned value is a tuple with the names of the columns and the result
    object.
    """
    query = """
    SELECT distinct 
                substring(to_char(total.day, 'YYYY-MM-DD') for 10)
                    AS day,
            total,
            errors,
            round((cast(errors AS decimal)*100)/total,2) AS percent
    FROM log 
    LEFT JOIN (
        SELECT date_trunc('day',time) as day, count(id) total
        FROM log
        GROUP BY day
        ) AS total
        ON date_trunc('day', log.time) = total.day
    LEFT JOIN (
        SELECT date_trunc('day',time) AS day, count(id) errors
        FROM log
        WHERE status = '404 NOT FOUND'
        GROUP BY day
        ) AS errors
    ON date_trunc('day', log.time) = errors.day
    WHERE %s <= round((cast(errors AS decimal)*100)/total,2)
    ORDER BY percent DESC
    ;
    """
    cur.execute(query, (topmost_percent,) )
    colnames = [desc[0] for desc in cur.description]
    return (colnames, cur.fetchall())


def report_line(row, title=False, just=50):
    """ Prints one line of a report to the console.

    Prints the line plus some ornamentation in order to make it easier to read.
    """
    n_items = len(row)
    if title:
        print '-'*(just*n_items+2*n_items+1)
    print "|",
    for c in row:
        print str(c).ljust(just), 
    print "|\n",
    if title:
        print '-'*(just*n_items+2*n_items+1)

def report(result, title=None, just=50):
    """ Prints one report to the console.

    Prints the result report (it does not execute the query) with some
    ornamentation to make it easier to read."""
    if title:
        print("\n\n\n==== "+title.upper()+' ====\n')
    cols, rows = result
    report_line(cols, title=True, just=just)
    for r in rows:
        report_line(r, just=just)
    print '-'*(just*len(cols)+2*len(cols)+1)

if __name__=='__main__':
    report(topArticles(), 'Top 3 most read articles')
    report(topAuthors(), 'Top 10 most read authors')
    report(topErrorsPerDay(), 'Top errors per day', 20)

db.close()
