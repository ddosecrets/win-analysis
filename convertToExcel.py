#!/usr/bin/env python3
import sqlite3
import pandas as pd

"""
	This script takes the 'win_network.db' SQLite3 database, and re-exports it
	as a series of excel spreadsheets. One sheet for all posts, and a sheet
	per site for comments. This fragmentation is necessary to avoid exceeding
	Excel's maximum row limits.
"""

conn = sqlite3.connect("win_network.db")
c = conn.cursor()
c.execute("SELECT DISTINCT site FROM comments")
sites = list(map(lambda s: s[0], c.fetchall()))
print("Found %d .Win sites..." % len(sites))
for site in sites:
	print("Exporting '%s' comments to Excel file..." % site)
	df_c = pd.read_sql_query("SELECT id,parent,site,author,timestamp,upvotes,downvotes,content FROM comments WHERE SITE=?", conn, params=[site])
	if( site == "thedonald" ):
		print("thedonald has too many comments to fit into an excel spreadsheet. Exporting to CSV instead (sorry!)")
		df_c.to_csv("comments_%s.csv" % site)
	else:
		df_c.to_excel("comments_%s.xlsx" % site)
print("Exporting posts to Excel file...")
df_p = pd.read_sql_query("SELECT id,title,author,content,timestamp,votes,site FROM posts", conn)
df_p.to_excel("posts.xlsx")
conn.close()
