## Win-Analysis

This codebase relates to the [.Win Network release](https://ddosecrets.com/wiki/.Win_Network) from Distributed Denial of Secrets.

The original release format is a newline-delimited JSON (NDJSON) file, where each line is a JSON blob representing a post or comment. Some researchers may prefer a database or spreadsheet format over the original JSON. This repository contains two utility scripts:

1. `convertToSQLite.py` converts the JSON to a SQLite3 database with two tables, one for comments and one for posts

2. `convertToExcel.py` converts the SQLite3 database to excel spreadsheets. One spreadsheet for all posts, and one spreadsheet per-site for comments. See "Excel Limitations" below for details.

### USAGE

First, [download the release](https://ddosecrets.com/wiki/.Win_Network), and place `win-network-full.ndjson` in the same directory as the provided Python scripts.

Second, install dependencies for this project:

    pip3 install -r requirements.txt

Or install them by hand. For exporting to SQLite3, you need only:

    pip3 install tqdm

While to export to Excel you will need:

    pip3 install tqdm pandas openpyxl

Finally, launch both scripts, like:

    ./convertToSQLite.py
    ./convertToExcel.py

### Original Schema

Here is an example comment:

	{
	  "_index": "win-data-000001",
	  "_type": "_doc",
	  "_id": "4DuTrcvVRkB",
	  "_score": 1,
	  "_source": {
		"v": 1,
		"html": ""REMOVED FROM README FOR LEGIBILITY",
		"author": "Zenmaster909",
		"parent": "11Rhher6Yh",
		"content": "Can any military confirm the wrinkled flag symbol? Do they do that? Are there other symbols and such they use?\nInteresting in this case, as well as generally...",
		"upvotes": 2,
		"downvotes": 0,
		"timestamp": 1610375547,
		"site": "greatawakening",
		"datatype": "comment",
		"html_parsed_html": "\n\n▲\n2\n▼\n\n\n\n–\n\r\n                    Zenmaster909\r\n                \n2 points\n53 minutes ago\n\n+2 / -0\n\n\n\nCan any military confirm the wrinkled flag symbol? Do they do that? Are there other symbols and such they use?\nInteresting in this case, as well as generally...\n\n\nparent\npermalink\nsave\nreport\nblock\nreply\n\n\n"
	  }
	}

And here is an example post:

	{
	  "_index": "win-data-000001",
	  "_type": "_doc",
	  "_id": "11S0SNGAlv",
	  "_score": 1,
	  "_source": {
		"v": 1,
		"html": "REMOVED FROM README FOR LEGIBILITY",
		"title": "It's Not Over!",
		"votes": 14,
		"author": "rosie",
		"content": "God isn't finished working yet.  That is all.",
		"timestamp": 1610509489,
		"site": "thedonald",
		"datatype": "post",
		"html_parsed_html": "\n\n\n\n\n14\n\n\n\n\n\n\n\n\n\n\n\r\n                    \r\n                    It's Not Over!\r\n                \n\n\nposted 4 minutes ago by rosie\n\n+14 / -0\n\n\n\n\nGod isn't finished working yet.  That is all.\n\nGod isn't finished working yet.  That is all.\n\n\n\n\n\n\n14\n\n\n\n\n 1 comment\nshare \n\n1 comment\nshare\nsave\nhide\nreport\nblock\nhide child comments\n\n\n\n\n\n\n\n\n\n\n\n\n"
	  }
	}

### Database Schema

The SQLite database retains the most critical fields, while dropping `_index`, `_type`, `v`, `datatype`, and `html_parsed_html`. The comments table has the schema:

	CREATE TABLE comments(
		id PRIMARY KEY,
		parent TEXT,
		site TEXT,
		author TEXT,
		timestamp INT,
		upvotes INT,
		downvotes INT,
		content TEXT,
		html TEXT);

While the posts table has the schema:

	CREATE TABLE posts(
		id PRIMARY KEY,
		title TEXT,
		author TEXT,
		content TEXT,
		timestamp INT,
		votes INT,
		site TEXT,
		html TEXT);

### Excel Limitations

The Excel spreadsheets have columns corresponding to the SQLite table fields. However, there are a few caveats:

1. The `html` field is dropped entirely, to keep spreadsheets small enough to not crash Excel, and to avoid weird parsing errors

2. The `thedonald` .Win site has too many comments to fit in an Excel spreadsheet, as it exceeds Excel's maximum row count. This site is exported as CSV instead.

3. Posts and comments containing URLs probably do not have these URLs formatted correctly

In general, the Excel export is of lower quality than the SQLite export, due to limitations in the Pandas library's Excel export functionality, the xlsx data format, and Microsoft Excel. This script is provided for convenience, but really, the SQLite export is preferable.
