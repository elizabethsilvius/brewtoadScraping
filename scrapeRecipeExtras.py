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

def getAmt(e_item):
    """
    This method gets the amount of an extra
    """
    try:
        return e_item.findAll('td')[0].text
    except:
        pass

def getExt(e_item):
    """
    This method gets the name of the extra
    """
    try:
        return e_item.findAll('td')[1].text.encode("UTF-8")
    except:
        pass

def getTime(e_item):
    """
    This method gets the time of an extra
    """
    try:
        return e_item.findAll('td')[2].text.encode("UTF-8")
    except:
        pass

def getUse(e_item):
    """
    This method gets the use of an extra
    """
    try:
        return e_item.findAll('td')[3].text.encode("UTF-8")
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS recipeExtras(inputNum PRIMARY KEY,
                      beerNum TEXT, RecipeName TEXT, Amount TEXT, Extra TEXT, 
                      Time TEXT, Use TEXT)
                      """)

def data_entry(number, beer, name, amt, ext, time,
                           use):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO recipeExtras(inputNum, beerNum,
                      RecipeName, Amount, Extra, 
                      Time, Use)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, beer, name, amt, ext, time,
                           use))
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
##                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'extras'}).find('tbody').find_all('tr')
##                for line in lines:
##                    rec_amt = getAmt(line)
##                    rec_ext = getExt(line)
##                    rec_time = getTime(line)
##                    rec_use = getUse(line)
##                    data_entry(k, rec_name, rec_amt, rec_ext, rec_time,
##                           rec_use)
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
