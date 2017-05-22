import dataset
import sqlite3
from bs4 import BeautifulSoup
import requests
import re


### ----------------------
### SETUP  
### ----------------------

conn = sqlite3.connect('brewtoad_new.db')
conn.text_factory = str
c = conn.cursor()


# ----------------------
# Methods for Scraping
# ----------------------

    
def getName(r_item):
    """
    This method gets the recipe name
    """
    try:
        return r_item.find("span", {"class": "name"}).text.encode('UTF-8')
    except:
        pass

def getStyle(r_item):
    """
    This method gets the recipe style
    """
    try:
        return r_item.find("span", {"class": "style"}).text.encode('UTF-8')
    except:
        pass

def getOG(r_item):
    """
    This method gets the recipe OG
    """
    try:
        return r_item.find("p", {"class": "og"}).text.encode('UTF-8').split("OG")[0]

    except:
        pass

def getFG(r_item):
    """
    This method gets the recipe FG
    """
    try:
        return r_item.find("p", {"class": "fg"}).text.encode('UTF-8').split("FG")[0]

    except:
        pass

def getIBU(r_item):
    """
    This method gets the recipe IBU
    """
    try:
        return r_item.find("p", {"class": "ibu"}).text.encode('UTF-8').split("IBU")[0]
    except:
        pass

def getABV(r_item):
    """
    This method gets the recipe ABV
    """
    try:
        return r_item.find("p", {"class": "abv"}).text.encode('UTF-8').split("ABV")[0]
    except:
        pass

def getType(r_item):
    """
    This method gets the recipe type
    """
    try:
        return r_item.find("p", {"class": "type"}).text.encode('UTF-8')
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS recipeBasics(inputNum PRIMARY KEY,
                      RecipeName TEXT, RecipeStyle TEXT, RecipeOG TEXT,
                      RecipeFG TEXT, RecipeIBU TEXT, RecipeABV TEXT,
                      RecipeType TEXT)
                      """)

def data_entry(number, name, style, og, fg, ibu,
                           abv, rectype):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO recipeBasics(inputNum,
                      RecipeName, RecipeStyle, RecipeOG,
                      RecipeFG, RecipeIBU, RecipeABV,
                      RecipeType)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, name, style, og, fg, ibu,
                           abv, rectype))
    conn.commit()

##def main():
##    create_table()
##    p = 4616
##    urls = ("https://www.brewtoad.com/recipes?page=1&sort=rank",
##            "https://www.brewtoad.com/recipes?page=2&sort=rank")
##    k = 138367
##    while p < 10052:
##        url = "https://www.brewtoad.com/recipes?page=%s&sort=rank" % p
##        r = requests.get(url)
##        soup = BeautifulSoup(r.content, "lxml")
##        recipes = soup.find_all("li", {"class": "recipe-container"})
##        for recipe in recipes:
##            try:
##                rec_name = getName(recipe)
##                rec_style = getStyle(recipe)
##                rec_og = getOG(recipe)
##                rec_fg = getFG(recipe)
##                rec_ibu = getIBU(recipe)
##                rec_abv = getABV(recipe)
##                rec_type = getType(recipe)
##                data_entry(k, rec_name, rec_style, rec_og, rec_fg, rec_ibu,
##                           rec_abv, rec_type)
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
