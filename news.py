#!/usr/bin/env python3

import psycopg2
import os

# Name the new database as news
DBNAME = "news"

# Open file
report = open("report.txt", "w")

# Access psql database news
db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# Query top three articles with views
c.execute("select * from page_views limit 3;")
pop_articles = c.fetchall()

# Write Q1 in the file
report.write("1. What are the most popular three articles of all time?\n")

# Iterate answers and write into file
for pop_articles in pop_articles:
    report.write("{article} --- {views} views\n".format(
                 article=pop_articles[0], views=pop_articles[1]))

# Query the popularity of authors
c.execute("""select author, sum(views) as pop_points from pop
          group by author order by pop_points desc;""")
pop_authors = c.fetchall()

# Write Q2 into files
report.write("2.Who are the most popular article authors of all time?\n")

# Iterate answers and write into file
for pop_author in pop_authors:
    report.write("{author}--{views} views\n".format(
                  author=pop_author[0], views=pop_author[1]))

# Query a date with more than 1% errors
c.execute("select date, pct_error from percentage where pct_error > 1.00;")
errors = c.fetchall()

# Write Q3 into file
report.write("3.On which days did more than 1% of requests lead to errors?\n")

# iterate answers and write into file
for error in errors:
    report.write("{date} -- {percentage}% errors\n".format(
                  date=error[0], percentage=error[1]))

# Close file
report.close()

# close the access to the database
db.close()
