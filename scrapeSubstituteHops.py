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

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS substituteHops(inputNum PRIMARY KEY,
                      Hopname TEXT, Substitute TEXT, Seller TEXT,
                      Vendor TEXT, SKU TEXT, Amount TEXT, Price TEXT,
                      ShippingWeight TEXT, BackOrdered TEXT)
                      """)

def data_entry(number, hop, name, seller, vend, sku,
                           amt, price, weight, back):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO substituteHops(inputNum, Hopname, Substitute,
                Seller, Vendor, SKU, Amount, Price, ShippingWeight, BackOrdered)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, hop, name, seller, vend, sku,
                           amt, price, weight, back))
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
            url_hop = "https://www.brewtoad.com" + getUrl(hop)
            h = requests.get(url_hop)
            soup_hop = BeautifulSoup(h.content, "lxml")
            hop_name = soup_hop.find("h1").text
            try:
                subs = soup_hop.find_all("div", {"class": "soft hard--top"})[2].find_all("li")
                for sub in subs:
                    sub_url = "https://www.brewtoad.com" + getUrl(sub)
                    s = requests.get(sub_url)
                    sub_page = BeautifulSoup(s.content, "lxml")
                    sub_name = sub_page.find("h1").text
                    dds = sub_page.find_all("dd")
                    sub_seller = dds[0].text
                    sub_vend = dds[1].text
                    sub_sku = dds[2].text
                    sub_amt = dds[3].text
                    sub_price = dds[4].text
                    sub_weight = dds[5].text
                    sub_back = dds[6].text
                    data_entry(k, hop_name, sub_name, sub_seller, sub_vend, sub_sku,
                               sub_amt, sub_price, sub_weight, sub_back)
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
