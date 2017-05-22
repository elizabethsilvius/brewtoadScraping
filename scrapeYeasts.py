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


def getYeast(y_item):
    """
    This method gets the yeast name on the yeasts page
    """
    try:
        return y_item.find("td").text.encode('UTF-8')
    except:
        pass

def getLab(y_item):
    """
    This method gets the yeast lab on the yeasts page
    """
    try:
        return y_item.find_all("td")[1].text.encode('UTF-8')
    except:
        pass

def getID(y_item):
    """
    This method gets the yeast product ID on the yeasts page
    """
    try:
        return y_item.find_all("td")[2].text.encode('UTF-8')
    except:
        pass

def getType(y_item):
    """
    This method gets the yeast typeon the yeasts page
    """
    try:
        return y_item.find_all("td")[3].text.encode('UTF-8')
    except:
        pass

def getTol(y_item):
    """
    This method gets the yeast alcohol tolerance on the yeasts page
    """
    try:
        return y_item.find_all("td")[4].text.encode('UTF-8')
    except:
        pass

def getFloc(y_item):
    """
    This method gets the yeast flocculation on the yeasts page
    """
    try:
        return y_item.find_all("td")[5].text.encode('UTF-8')
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS yeasts(inputNum PRIMARY KEY,
                      name TEXT, laboratory TEXT, product_id TEXT,
                      yeast_type TEXT, alcohol_tolerance TEXT,
                      flocculation TEXT)
                      """)

def data_entry(number, yeast, lab, prodid, ytype, altol,
               flocc):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO yeasts (inputNum, name, laboratory,
                product_id, yeast_type, alcohol_tolerance,
                      flocculation) VALUES(?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, yeast, lab, prodid, ytype, altol,
               flocc))
    conn.commit()

def main():
    create_table()
    urls = ("https://www.brewtoad.com/yeasts", "https://www.brewtoad.com/yeasts?page=2",
           "https://www.brewtoad.com/yeasts?page=3",
           "https://www.brewtoad.com/yeasts?page=4",
           "https://www.brewtoad.com/yeasts?page=5")
    k = 1
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        yeasts = soup.find("table").find('tbody').find_all("tr")
        for yeast in yeasts:
            yeast_name = getYeast(yeast)
            yeast_lab = getLab(yeast)
            yeast_id = getID(yeast)
            yeast_type = getType(yeast)
            yeast_tol = getTol(yeast)
            yeast_flocc = getFloc(yeast)
            data_entry(k, yeast_name, yeast_lab, yeast_id,
               yeast_type, yeast_tol, yeast_flocc)
            k = k+1
            
    c.close()
    conn.close()

# ----------------------
# Start Scraping 
# ----------------------

if __name__ == "__main__":
    main()
