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
        return "https://www.brewtoad.com" + s_item.find('a').get("href")
    except:
        pass
    
def getName(r_item):
    """
    This method gets the recipe name
    """
    try:
        return r_item.find("span", {"class": "name"}).text.encode('UTF-8')
    except:
        pass

def getBatch(s_item):
    """
    This method gets the batch size
    """
    try:
        return s_item.text.encode("UTF-8").split("Batch Size")[1].split("Boil Time")[0]
    except:
        pass

def getBoil(s_item):
    """
    This method gets the boil time
    """
    try:
        return s_item.text.encode("UTF-8").split("Boil Time")[1].split("More")[0]
    except:
        pass

def getEff(s_item):
    """
    This method gets the efficiency
    """
    try:
        return s_item.text.encode("UTF-8").split("Efficiency")[1].split("Fermentation")[0]
    except:
        pass

def getPrim(s_item):
    """
    This method gets the length of the primary fermentation
    """
    try:
        return s_item.text.encode("UTF-8").split("Primary")[1].split("Secondary")[0]
    except:
        pass

def getSec(s_item):
    """
    This method gets the length of the secondary fermentation
    """
    try:
        return s_item.text.encode("UTF-8").split("Secondary")[1].split("Misc.")[0]
    except:
        pass

def getIBU(s_item):
    """
    This method gets the IBU Formula
    """
    try:
        return s_item.text.encode("UTF-8").split("IBU Formula")[1]
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS recipeStats(inputNum PRIMARY KEY,
                      beerNum TEXT,
                      RecipeName TEXT, BatchSize TEXT, BoilTime TEXT, 
                      Efficiency TEXT, PrimaryFermentation TEXT,
                      SecondaryFermentation TEXT, IBUFormula TEXT)
                      """)

def data_entry(number, beer, name, batch, boil, eff, prim, sec,
                           ibu):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO recipeStats(inputNum, beerNum,
                      RecipeName, BatchSize, BoilTime, 
                      Efficiency, PrimaryFermentation,
                      SecondaryFermentation, IBUFormula)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, beer, name, batch, boil, eff, prim, sec,
                           ibu))
    conn.commit()

##def main():
##    create_table()
##    p = 1
##    k = 1
##    while p < 10052:
##        url = "https://www.brewtoad.com/recipes?page=%s&sort=rank" % p
##        r = requests.get(url)
##        soup = BeautifulSoup(r.content, "lxml")
##        recipes = soup.find_all("li", {"class": "recipe-container"})
##        for recipe in recipes:
##            rec_url = getUrl(recipe)
##            rec_name = getName(recipe)
##            page = requests.get(rec_url)
##            pagesoup = BeautifulSoup(page.content, "lxml")
##            try:
##                lines = pagesoup.find('body').find('div',{'class': 'soft'})
##                rec_batch = getBatch(lines)
##                rec_boil = getBoil(lines)
##                rec_eff = getEff(lines)
##                rec_prim = getPrim(lines)
##                rec_sec = getSec(lines)
##                rec_ibu = getIBU(lines)
##                data_entry(k, rec_name, rec_batch, rec_boil, rec_eff,
##                        rec_prim, rec_sec, rec_ibu)
##                k = k + 1
##            except:
##                pass
##        p = p + 1
##    c.close()
##    conn.close()
##
### ----------------------
### Start Scraping 
### ----------------------
##
##if __name__ == "__main__":
##    main()
