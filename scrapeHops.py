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
        return s_item.find('a').get("href")
    except:
        pass

def getHop(h_item):
    """
    This method gets the hop name on the hops page
    """
    try:
        return h_item.find("td").text.encode('UTF-8')
    except:
        pass

def getCountry(h_item):
    """
    This method gets the hop country on the hops page
    """
    try:
        return h_item.find_all("td")[1].text.encode('UTF-8')
    except:
        pass

def getAlphaMin(h_item):
    """
    This method gets the minimum of the alphas
    """
    try:
        alpha = h_item.find_all("td")[2].text.encode('UTF-8')
        dist = re.findall("[-+]?\d+[\.]?\d+[eE]?[-+]?\d*", alpha)
        return dist[0]
    except:
        pass

def getAlphaMax(h_item):
    """
    This method gets the maximum of the alphas
    """
    try:
        alpha = h_item.find_all("td")[2].text.encode('UTF-8')
        dist = re.findall("[-+]?\d+[\.]?\d+[eE]?[-+]?\d*", alpha)
        return dist[1]
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS hops(inputNum PRIMARY KEY,
                      name TEXT, country TEXT, alpha_min TEXT,
                      alpha_max TEXT)
                      """)

def data_entry(number, hops_name, hops_country, hops_alpha_min,
               hops_alpha_max):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO hops (inputNum, name, country,
                    alpha_min, alpha_max) VALUES(?, ?, ?, ?, ?)
                    """,
              (number, hops_name, hops_country, hops_alpha_min,
               hops_alpha_max))
    conn.commit()

def main():
    create_table()
    urls = ("https://www.brewtoad.com/hops", "https://www.brewtoad.com/hops?page=2",
           "https://www.brewtoad.com/hops?page=3",
           "https://www.brewtoad.com/hops?page=4",
           "https://www.brewtoad.com/hops?page=5")
    k = 1
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        hops = soup.find("table").find('tbody').find_all("tr")
        for hop in hops:
            hop_name = getHop(hop)
            hop_country = getCountry(hop)
            hop_alpha_min = str(getAlphaMin(hop))
            hop_alpha_max = str(getAlphaMax(hop))
            data_entry(k, hop_name, hop_country, hop_alpha_min,
               hop_alpha_max)
            k = k+1
            
    c.close()
    conn.close()

# ----------------------
# Start Scraping 
# ----------------------

if __name__ == "__main__":
    main()
