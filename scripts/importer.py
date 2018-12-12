import csv
import sqlite3 as sqlite
from sqlite3 import Error

def create_soccer_db():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite.connect('soccerDB.sqlite')
        print(sqlite.version)
    except Error as e:
        print(e)

    cur = conn.cursor()


    '''
    Drop Tables
    '''
    statement = '''
        DROP TABLE IF EXISTS 'Leagues';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Players';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Teams';
    '''
    cur.execute(statement)


    '''
    Create Tables
    '''

    statement = '''
        CREATE TABLE 'Leagues' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'NumberOfTeams' TEXT NOT NULL,
            'NumberOfPlayers' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Teams' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Nickname' TEXT NOT NULL,
            'Squad' INTEGER NOT NULL,
            'AverageAge' REAL NOT NULL,
            'NumberofForeigners' INTEGER NOT NULL,
            'TotalMarketValue' INTEGER NOT NULL,
            'AverageMarketValue' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Players' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'JerseyNumber' INTEGER NOT NULL,
            'Name' TEXT NOT NULL,
            'Position' TEXT NOT NULL,
            'Birthday' TEXT NOT NULL,
            'Nationality' TEXT NOT NULL,
            'Team' TEXT NOT NULL,
            'Market Value' INTEGER NOT NULL,
            FOREIGN KEY(Team) REFERENCES Teams(Name)
        );
    '''
    
    cur.execute(statement)


    conn.close()

def populate_soccer_db():
    # Connect to soccer database
    conn = sqlite.connect('soccerDB.sqlite')
    cur = conn.cursor()

    with open('leagues.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
                insertion = (None, row[0], row[1], row[2])
                statement = 'INSERT INTO "Leagues" '
                statement += 'VALUES (?, ?, ?, ?)'
                cur.execute(statement, insertion)

    with open('teams.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            #Code to Clean CSV
            row[3] = float(row[3].replace(',','.'))

            #Total Market Value
            if 'Bill' in row[5]:
                row[5] = row[5][:-8]
                row[5] += '0,000,000' #billion string
                row[5] = row[5].replace(',','')
                row[5] = int(row[5])
            elif 'Mill' in row[5]:
                row[5] = row[5][:-8]
                row[5] += '0,000' #million string
                row[5] = row[5].replace(',','')
                row[5] = int(row[5])

            #Average Market Value
            if 'Bill' in row[6]:
                row[6] = row[6][:-8]
                row[6] += '0,000,000' #billion string
                row[6] = row[6].replace(',','')
                row[6] = int(row[6])
            elif 'Mill' in row[6]:
                row[6] = row[6][:-8]
                row[6] += '0,000' #million string
                row[6] = row[6].replace(',','')
                row[6] = int(row[6])

            insertion = (None, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            statement = 'INSERT INTO "Teams" '
            statement += 'VALUES (?, ?, ?, ?, ?, ? ,?, ?)'
            cur.execute(statement, insertion)
    
    with open('players.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if 'Mill' in row[6]:
                row[6] = row[6][:-10]
                row[6] += '0,000' #million string
                row[6] = row[6].replace(',','')
                row[6] = int(row[6])
            elif 'Th' in row[6]:
                row[6] = row[6][:-8]
                row[6] += '000' #thousand string
                row[6] = row[6].replace(',','')
                row[6] = int(row[6])

            insertion = (None, row[0], row[1], row[2], row[3],row[4],row[5],row[6])
            statement = 'INSERT INTO "Players" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?,?,?)'
            cur.execute(statement, insertion)
    # Close connection
    conn.commit()
    conn.close()

def test_csv():
    with open('players.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if 'Th' in row[6]:
                row[6] = row[6][:-8]
                row[6] += '000' #thousand string
                row[6] = row[6].replace(',','')
                row[6] = int(row[6])
                print(row[6])


if __name__ == "__main__":
    create_soccer_db()
    print("Created soccer Database")
    populate_soccer_db()
    print("Populated soccer Database")
    '''
    test_csv()
    '''