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

def getStep(m_item):
    """
    This method gets the step of the mash
    """
    try:
        return m_item.findAll('td')[0].text
    except:
        pass

def getSource(m_item):
    """
    This method gets the eat source of a mash step
    """
    try:
        return m_item.findAll('td')[1].text.encode("UTF-8").lstrip(" ")
    except:
        pass

def getTemp(m_item):
    """
    This method gets the target temp of a mash step
    """
    try:
        return m_item.findAll('td')[2].text.encode("UTF-8").split(" ")[0]
    except:
        pass

def getTime(m_item):
    """
    This method gets the target time of a mash step
    """
    try:
        return m_item.findAll('td')[3].text.encode("UTF-8")
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS recipeMash(inputNum PRIMARY KEY,
                      beerNum TEXT, 
                      RecipeName TEXT, MashStep TEXT, HeatSource TEXT, 
                      TargetTemp TEXT, Time TEXT)
                      """)

def data_entry(number, beer, name, step, heat, temp, time):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO recipeMash(inputNum, beerNum,
                      RecipeName, MashStep, HeatSource, 
                      TargetTemp, Time)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, beer, name, step, heat, temp, time))
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
##                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'mash_steps'}).find('tbody').find_all('tr')
##                for line in lines:
##                    rec_step = getStep(line)
##                    rec_heat = getSource(line)
##                    rec_temp = getTemp(line)
##                    rec_time = getTime(line)
##                    data_entry(k, rec_name, rec_step, rec_heat,
##                           rec_temp, rec_time)
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
