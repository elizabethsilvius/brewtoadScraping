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

def getAmt(h_item):
    """
    This method gets the amount of a fermentable
    """
    try:
        return h_item.findAll('td')[0].text.encode('UTF-8')
    except:
        pass

def getHop(h_item):
    """
    This method gets the name of a hop
    """
    try:
        return h_item.findAll('td')[1].text.encode("UTF-8").lstrip(" ")
    except:
        pass

def getTime(h_item):
    """
    This method gets the time of a hop
    """
    try:
        return h_item.findAll('td')[2].text.encode("UTF-8")
    except:
        pass

def getUse(h_item):
    """
    This method gets the use of a hop
    """
    try:
        return h_item.findAll('td')[3].text.encode("UTF-8")
    except:
        pass

def getForm(h_item):
    """
    This method gets the form of a hop
    """
    try:
        return h_item.findAll('td')[4].text.encode("UTF-8")
    except:
        pass

def getAA(h_item):
    """
    This method gets the AA a hop
    """
    try:
        return h_item.findAll('td')[5].text.encode("UTF-8").split('%')[0]
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS recipeHops(inputNum PRIMARY KEY,
                      beerNum TEXT,
                      RecipeName TEXT, HopAmt TEXT, HopName TEXT, HopTime TEXT,
                      HopUse TEXT,
                      HopForm TEXT, HopAA TEXT)
                      """)

def data_entry(number, beer, name, amt, hop, time, use, form,
                       aa):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO recipeHops(inputNum, beerNum,
                      RecipeName, HopAmt, HopName, HopTime, HopUse,
                      HopForm, HopAA)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, beer, name, amt, hop, time, use,
                       form, aa))
    conn.commit()

##def main():
##    create_table()
##    #skipping 4968 and part of 4967
##    p = 4969
##    k = 519713
##    while p < 10052:
##        url = "https://www.brewtoad.com/recipes?page=%s&sort=rank" % p
##        r = requests.get(url)
##        soup = BeautifulSoup(r.content, "lxml")
##        recipes = soup.find_all("li", {"class": "recipe-container"})
##        for recipe in recipes:
##            rec_url = getUrl(recipe)
##            rec_name = getName(recipe)
##            try:
##                page = requests.get(rec_url)
##                pagesoup = BeautifulSoup(page.content, "lxml")
##                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'hops'}).find('tbody').find_all('tr')
##                for line in lines:
##                    rec_amt = getAmt(line)
##                    rec_hop = getHop(line)
##                    rec_use = getUse(line)
##                    rec_form = getForm(line)
##                    rec_aa = getAA(line)
##                    data_entry(k, rec_name, rec_amt, rec_hop, rec_use,
##                           rec_form, rec_aa)
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
