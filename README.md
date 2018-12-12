# TransferMarket-python networkViz

## Description
The goal of this project is to scrape and crawl through multiple pages of [TransferMarket.com](https://www.transfermarkt.com/) and create an interesting Network Visualization  

### Possible Libraries
[Bokeh](https://bokeh.pydata.org/en/latest/)
[NetworkX](https://networkx.github.io/documentation/stable/index.html)



## Project Layout
    ├── data                      # Folder for Generated JSON Cache, CSVs, and SQLite Database
    ├── scripts                   # Crawling/Scraping Script, Database Importer Script
    ├── queries.py                # SQLite Database Queries that returns a list of tuples
    └── README.md

## Install Required Dependencies
Install and Enter your Virtual Environment
```
pip install virtualenv #if you don't have virtualenv installed 

virtualenv <Name_of_Virtual_Environment>
source <Name_of_Virtual_Environment>/bin/activate
```

Install project requirements
```
pip install -r requirements.txt
```

## Getting Started
Run scraper.py to scrape websites and create CSVs
```
cd data
python3 ../scripts/scraper.py
```

Run import.py to import CSVs into SQLite database
```
cd data
python3 ../scripts/importer.py
```

Move the created database from data/ to the main project folder
```
cd <Main Project Folder>
mv data/soccerDB.sqlite ./
```
or
```
cd data
mv soccerDB.sqlite ../