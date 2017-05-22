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

def getAmt(f_item):
    """
    This method gets the amount of a fermentable
    """
    try:
        return f_item.findAll('td')[0].text
    except:
        pass

def getFerm(f_item):
    """
    This method gets the name of a fermentable
    """
    try:
        return f_item.findAll('td')[1].text.encode("UTF-8").lstrip(" ")
    except:
        pass

def getMalt(f_item):
    """
    This method gets the maltster of a fermentable
    """
    try:
        return f_item.findAll('td')[2].text.encode("UTF-8")
    except:
        pass

def getUse(f_item):
    """
    This method gets the use of a fermentable
    """
    try:
        return f_item.findAll('td')[3].text.encode("UTF-8")
    except:
        pass

def getPPG(f_item):
    """
    This method gets the PPG of a fermentable
    """
    try:
        return f_item.findAll('td')[4].text.encode("UTF-8")
    except:
        pass

def getCol(f_item):
    """
    This method gets the colof a fermentable
    """
    try:
        return f_item.findAll('td')[5].text.encode("UTF-8").split(" ")[0]
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS recipeFermentables(inputNum PRIMARY KEY,
                      beerNum TEXT, RecipeName TEXT, FermAmt TEXT, FermName TEXT, FermMalt TEXT,
                      FermUse TEXT, FermPPG TEXT, FermCol TEXT)
                      """)

def data_entry(number, beer, name, amt, ferm, malt, use,
                       ppg, col):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO recipeFermentables(inputNum, beerNum,
                      RecipeName, FermAmt, FermName, FermMalt,
                      FermUse, FermPPG, FermCol)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, beer, name, amt, ferm, malt, use,
                       ppg, col))
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
##                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'fermentables'}).find('tbody').find_all('tr')
##                for line in lines:
##                    rec_amt = getAmt(line)
##                    rec_ferm = getFerm(line)
##                    rec_malt = getMalt(line)
##                    rec_use = getUse(line)
##                    rec_ppg = getPPG(line)
##                    rec_col = getCol(line)
##                    data_entry(k, rec_name, rec_amt, rec_ferm, rec_malt, rec_use,
##                           rec_ppg, rec_col)
##                    k = k + 1
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
