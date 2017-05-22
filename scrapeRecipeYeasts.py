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

def getYeast(y_item):
    """
    This method gets the name of a yeast
    """
    try:
        return y_item.findAll('td')[0].text.encode("UTF-8")
    except:
        pass

def getLab(y_item):
    """
    This method gets the lab of a yeast
    """
    try:
        return y_item.findAll('td')[1].text.encode("UTF-8").lstrip(" ")
    except:
        pass

def getAtt(y_item):
    """
    This method gets the attenuation of a yeast
    """
    try:
        return y_item.findAll('td')[2].text.encode("UTF-8")
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS recipeYeast(inputNum PRIMARY KEY,
                      beerNum TEXT,
                      RecipeName TEXT, YeastName TEXT, LabProduct TEXT, 
                      Attenuation TEXT)
                      """)

def data_entry(number, beer, name, yeast, lab, att):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO recipeYeast(inputNum, beerNum,
                      RecipeName, YeastName, LabProduct,
                      Attenuation)
                VALUES(?, ?, ?, ?, ?, ?)
                    """,
              (number, beer, name, yeast, lab, att))
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
##            try:    
##                page = requests.get(rec_url)
##                pagesoup = BeautifulSoup(page.content, "lxml")
##                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'yeasts'}).find('tbody').find_all('tr')
##                for line in lines:
##                    rec_yeast = getYeast(line)
##                    rec_lab = getLab(line)
##                    rec_att = getAtt(line)
##                    data_entry(k, rec_name, rec_yeast, rec_lab,
##                           rec_att)
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
