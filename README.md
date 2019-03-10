# 2018 International Football TransferMarket Visualization in Bokeh

<p align="middle">
    <img src="https://github.com/hopetambala/dataViz-bokeh-transferMarkt/blob/master/docs/scatter.png">
</p>


## Demos
[Interactive Chart](https://hopetambala.github.io/dataViz-bokeh-transferMarkt/docs/scatterPlot.html)
## Description
The goal of this project is to scrape and crawl through multiple pages of [TransferMarket.com](https://www.transfermarkt.com/) and create an interesting Bokeh Visualization. The data was scrapped using BeautifulSoup and compiled into a SQLite database. Then SQL queries were constructed and the query results were loaded into a Pandas to allow for easier data manipulation. Finally, that data was loaded into Bokeh to create a Scatter Plot that explores the relationships between a soccer teams 
A) Average Squad Age 
B) 2018 Squad Market Value and 
C) Number of Foreign Players found in each Squad.

### Data Visualization Libraries
[Bokeh](https://bokeh.pydata.org/en/latest/)


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

Install Bokeh
```
pip install bokeh
```

Install Bokeh
```
pip install pandas
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
```

## Run

```
python main.py
```

## Resources

#Pandas and Sqlite
https://www.dataquest.io/blog/python-pandas-databases/

#Pandas and Bokeh
https://programminghistorian.org/en/lessons/visualizing-with-bokeh


# Tutorial

## Key Functions

### Get Teams using pandas_get_teams() in queries.py
```
statement = '''
    SELECT * from Teams
    ORDER BY Teams.TotalMarketValue DESC; 
    '''
conn = sqlite.connect('soccerDB.sqlite')
df = pd.read_sql_query(statement, conn)
return df 
```
This above function uses Pandas "read_sql_query()" function to automatically load the results of a SQL query into a database. Very easy to use 

### Load Data Into Bokeh
```
df = pandas_get_teams()
...
source = ColumnDataSource(df)
```

### Color Mapper
```
palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0","#f7f7f7", "#fddbc7","#f4a582", "#d6604d", "#b2182b", "#67001f"]

AverageAge = df["AverageAge"]

low = min(AverageAge)
high = max(AverageAge)
AverageAge_inds = [int(10*(x-low)/(high-low)) for x in AverageAge]

df['age_colors'] = [palette[i] for i in AverageAge_inds]

color_mapper = LogColorMapper(palette=palette, low=low, high=high)
```
In order to map the average squad ages to one of the colors found in the palette list:
- Use Numpy's min/max functions to get the minimum/maximum of the list of squad ages
- Create a list (using list comprehension) to give average age a value from 0-10 and
- Create a Pandas Column that attaches each one of the the palette colors to a row in our df.

# Key Takeaways 
Bokeh is great for rapid data visualization development. It's simple to use especially when using a Pandas Dataframe to manage your data! To style your application, there are a variety of [widgets](https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/widgets.html) to add and expand interactive funcitonality.

The actual visualization generated comes with alot of built-in interactive abilities that don't need to be coded in. You can save a png of your graph for instant sharing and zoom in/out or pan the visualization without explicitly writing code to add those functionalities!

# Limitations
Bokeh isn't really python-only. It generates an HTML file with your visualization on it. Potentially useful for web development environmenta.s



