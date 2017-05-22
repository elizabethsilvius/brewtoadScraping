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



def getExtra(e_item):
    """
    This method gets the extra name on the extras page
    """
    try:
        return e_item.find("td").text.encode('UTF-8')
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS extras(inputNum PRIMARY KEY,
                      name TEXT)
                      """)

def data_entry(number, extras_name):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO extras (inputNum, name) VALUES(?, ?)
                    """,
              (number, extras_name))
    conn.commit()

def main():
    create_table()
    urls = ("https://www.brewtoad.com/extras", "https://www.brewtoad.com/extras?page=2",
           "https://www.brewtoad.com/extras?page=3",
           "https://www.brewtoad.com/extras?page=4",
           "https://www.brewtoad.com/extras?page=5")
    k = 1
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        extras = soup.find("table").find('tbody').find_all("tr")
        for extra in extras:
            ex_name = getExtra(extra)
            data_entry(k, ex_name)
            k = k+1
            
    c.close()
    conn.close()

# ----------------------
# Start Scraping 
# ----------------------

if __name__ == "__main__":
    main()
