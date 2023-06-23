# cpiProject
This project is meant to build an analysis of inflation in the U.S.

The current code:
  1) Jupyter notebook and a .py file that create a database of selected U.S. Bureau of Labor Statistics (BLS) data.
  2) A simple app that intakes BLS time series id's and descriptions and inserts them into a table.

The app was discarded as a solution, but I'm publishing it as an interesting example of my coding ability.

In order to create the database usinge either blsDatabaseCreation.ipynb or blsDatabaseCreation.py:

1. Download the files below (the BLS doesn't make it easy to scrape):

https://download.bls.gov/pub/time.series/ap/ap.data.0.Current  
https://download.bls.gov/pub/time.series/ap/ap.series  
https://download.bls.gov/pub/time.series/cu/cu.data.0.Current  
https://download.bls.gov/pub/time.series/cu/cu.series  

Manually download these files by visiting the page and right-clicking; these files are too big to load in your browser, and the BLS restricts scraping (but does not specify under what circumstances a scraper would be allowed.) If you are aware of how to get an automated download of this data going that would simplify things for anyone who wants to repeat what I've done here.

2. Set up a Postgresql instance: https://www.postgresql.org/ 

3. Modify the blsDatabaseCreation.py or blsDatabaseCreation.ipynb file to point at the right filepaths for your downloads and host/port/database path for your Postgresql server. 

From there, run the code and watch it work. I used chunking to speed up the runtime. If this was a real project I'd probably handle the database creation completely in SQL but I wrapped it in Python to make it easy to read. 

The code depends upon Python 3.9.13 and the Jupyter kernel if applicable.

Please email the author with questions.
