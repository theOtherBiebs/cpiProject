# cpiProject
This project is meant to build an analysis of inflation in the U.S.

The first code published will be both a Jupyter notebook and a .py file that create a database of selected U.S. Bureau of Labor Statistics (BLS) data.

The download links for the necessary text files are located:

https://download.bls.gov/pub/time.series/ap/ap.data.0.Current  
https://download.bls.gov/pub/time.series/ap/ap.series  
https://download.bls.gov/pub/time.series/cu/cu.data.0.Current  
https://download.bls.gov/pub/time.series/cu/cu.series  

You'll have your best luck manually downloading these files by visiting the page and right-clicking; these files are too big to load in your browser, and the BLS restricts scraping (but does not specify under what circumstances a scraper would be allowed.) If you are aware of how to get an automated download of this data going that would simplify things for anyone who wants to repeat what I've done here.

Once you've downloaded the above files, you'll need to set up a Postgresql instance. 

You can do that here: https://www.postgresql.org/ 

It's pretty trivial. The documentation on the above site will make it quite easy.

Once you have a Postgresql server going, you can modify the blsDatabaseCreation.py or blsDatabaseCreation.ipynb file to point at the right filepaths for your downloads and host/port/database path for your Postgresql server. 

From there, run the code and watch it work. Runtime is long; If you know anyone at the BLS who would hand out a contract to improve their API to make this all redundant I'd love to meet them. 

Email the author with questions.
