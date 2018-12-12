# transferMarket-python networkViz

## Install Required Dependencies
Install and Enter Virtual Environment
```
virtualenv venv
source venv/bin/activate
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