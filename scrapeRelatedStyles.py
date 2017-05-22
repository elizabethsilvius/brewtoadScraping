import dataset
import sqlite3
from bs4 import BeautifulSoup
import requests
import re


# ----------------------
# SETUP  
# ----------------------

conn = sqlite3.connect('brewtoad_new2.db')
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

def getRelated(l_item):
    """
    This method gets the realted styles on a stats page
    """
    try:
        return l_item.text.encode('UTF-8').split("Type")[1]
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS relatedStyles(inputNum PRIMARY KEY,
                      name TEXT, related TEXT)
                      """)

def data_entry(number, style_name, related_style):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO relatedStyles (inputNum, name, related)
                VALUES(?, ?, ?)
                    """,
              (number, style_name, related_style))
    conn.commit()

def main():
    create_table()
    url = ("https://www.brewtoad.com/styles")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    styles = soup.find("table", {"id": "styles"}).find('tbody').find_all("tr")
    k = 1
    for style in styles:
        url_style = "https://www.brewtoad.com" + getUrl(style)
        s = requests.get(url_style)
        soup_style = BeautifulSoup(s.content, "lxml")
        stat_name = soup_style.find("header").find("h1").text
        try:
            relats = soup_style.find_all("div", {"class": "soft hard--bottom"})
            rel_styles = relats[1].find_all("li")
            for rs in rel_styles:
                data_entry(k, stat_name, rs.text)
                k = k+1
        except:
            pass
    c.close()
    conn.close()

# ----------------------
# Start Scraping 
# ----------------------

if __name__ == "__main__":
    main()
