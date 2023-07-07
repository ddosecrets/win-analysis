#!/usr/bin/env python3
import sqlite3, json
from tqdm import tqdm

"""
	This script takes a "win-network-full.ndjson" file, extracts the comments
	and posts, and saves them to a sqlite "win_network.db" file for easier
	access. The original "win-network-full.ndjson" can be downloaded here:
		https://ddosecrets.com/wiki/.Win_Network
	Download the file, then unzip it, then run this script.
"""

COMMENTS_SCHEMA = """CREATE TABLE IF NOT EXISTS comments(
	id PRIMARY KEY,
	parent TEXT,
	site TEXT,
	author TEXT,
	timestamp INT,
	upvotes INT,
	downvotes INT,
	content TEXT,
	html TEXT)
"""

POSTS_SCHEMA = """CREATE TABLE IF NOT EXISTS posts(
	id PRIMARY KEY,
	title TEXT,
	author TEXT,
	content TEXT,
	timestamp INT,
	votes INT,
	site TEXT,
	html TEXT)
"""

ENTRIES = 1828910

with open("win-network-full.ndjson", "r") as f:
	conn = sqlite3.connect("win_network.db")
	c = conn.cursor()
	c.execute(COMMENTS_SCHEMA)
	c.execute(POSTS_SCHEMA)
	pbar = tqdm(total=ENTRIES, desc="Parsing entries")
	for line in f:
		data = json.loads(line)
		_id = data["_id"]
		datatype = data["_source"]["datatype"]
		author = data["_source"]["author"]
		site = data["_source"]["site"]
		content = data["_source"]["content"]
		html = data["_source"]["html"]
		ts = int(data["_source"]["timestamp"])
		if( datatype == "comment" ):
			upvotes = int(data["_source"]["upvotes"])
			downvotes = int(data["_source"]["downvotes"])
			parent = data["_source"]["parent"]
			c.execute("INSERT OR IGNORE INTO comments (id,parent,site,author,timestamp,upvotes,downvotes,content,html) VALUES(?,?,?,?,?,?,?,?,?)",
				[_id,parent,site,author,ts,upvotes,downvotes,content,html])
		elif( datatype == "post" ):
			title = data["_source"]["title"]
			votes = int(data["_source"]["votes"])
			c.execute("INSERT OR IGNORE INTO posts (id,title,site,author,timestamp,votes,content,html) VALUES(?,?,?,?,?,?,?,?)",
				[_id,title,site,author,ts,votes,content,html])
		else:
			print("Unexpected data type '%s'" % datatype)
		pbar.update(1)
	pbar.close()
	conn.commit()
	conn.close()
