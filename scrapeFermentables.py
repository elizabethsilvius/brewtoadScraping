import dataset
import sqlite3
from bs4 import BeautifulSoup
import requests
import re


# ----------------------
# SETUP  
# ----------------------

conn = sqlite3.connect('brewtoad_new.db')
conn.text_factory = str
c = conn.cursor()


# ----------------------
# Methods for Scraping
# ----------------------

    
def getUrl(s_item):
    """
    This method gets the url for each style
    """
    try:
        return s_item.find('a').get("href")
    except:
        pass

def getFerment(l_item):
    """
    This method gets the name of a fermentable 
    """
    try:
        return l_item.find_all("td")[0].text.encode("UTF-8")
    except:
        pass
    
def getType(l_item):
    """
    This method gets the type on a fermentable page
    """
    try:
        return l_item.find_all("td")[1].text.encode("UTF-8")
    except:
        pass

def getCol(l_item):
    """
    This method gets the color on a fermentable page
    """
    try:
        cols = l_item.find_all("td")[2].text.encode("UTF-8")
        cols_new = [int(s) for s in cols.split() if s.isdigit()]
        return str(cols_new[0])
    except:
        pass

def getPPG(l_item):
    """
    This method gets the ppg on a fermentable page
    """
    try:
        return l_item.find_all("td")[3].text.encode("UTF-8")
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS fermentables(inputNum PRIMARY KEY,
                      name TEXT, type TEXT, color TEXT,
                      ppg TEXT)
                      """)

def data_entry(number, fermentable_name, fermentable_type, fermentable_col,
               fermentable_ppg):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO fermentables (inputNum, name, type,
                    color, ppg) VALUES(?, ?, ?, ?, ?)
                    """,
              (number, fermentable_name, fermentable_type,
               fermentable_col, fermentable_ppg))
    conn.commit()

def main():
    create_table()
    url = ("https://www.brewtoad.com/generic-fermentables")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    ferments = soup.find("table", {"id": "fermentables"}).find('tbody').find_all("tr")
    k = 1
    for ferment in ferments:
        #url_style = "https://www.brewtoad.com" + getUrl(style)
        #s = requests.get(url_style)
        #soup_style = BeautifulSoup(s.content, "lxml")
        ferment_name = getFerment(ferment)
        ferment_type = getType(ferment)
        ferment_col = getCol(ferment)
        ferment_ppg = getPPG(ferment)
        data_entry(k, ferment_name, ferment_type, ferment_col, ferment_ppg)
        k = k+1
            
    c.close()
    conn.close()

# ----------------------
# Start Scraping 
# ----------------------

if __name__ == "__main__":
    main()
