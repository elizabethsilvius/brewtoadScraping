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

def getType(l_item):
    """
    This method gets the type on a stats page
    """
    try:
        return l_item.text.encode('UTF-8').split("Type")[1]
    except:
        pass

def getMin(l_item, stat_name):
    """
    This method gets the minimum of a stat
    """
    try:
        stat = l_item.text.encode('UTF-8').split(stat_name)[1]
        dist = re.findall("[-+]?\d+[\.]?\d+[eE]?[-+]?\d*", stat)
        return dist[0]
    except:
        pass

def getMax(l_item, stat_name):
    """
    This method gets the maximum of a stat
    """
    try:
        stat = l_item.text.encode('UTF-8').split(stat_name)[1]
        dist = re.findall("[-+]?\d+[\.]?\d+[eE]?[-+]?\d*", stat)
        return dist[1]
    except:
        pass

def create_table():
    """
    This method creates a table
    """
    c.execute("""\
                CREATE TABLE IF NOT EXISTS styles(inputNum PRIMARY KEY,
                      name TEXT, type TEXT, og_average TEXT,
                      fg_average TEXT, ibu_average TEXT,
                      color_average TEXT, abv_average TEXT, og_min TEXT,
                      og_max TEXT, fg_min TEXT, fg_max TEXT,
                      ibu_min TEXT, ibu_max TEXT, color_min TEXT,
                      color_max TEXT, abv_min TEXT, abv_max TEXT)
                      """)

def data_entry(number, style_name, style_type, style_og_avg, style_fg_avg,
                           style_ibu_avg, style_col_avg, style_abv_avg,
                           style_og_min, style_og_max,
                           style_fg_min, style_fg_max, style_ibu_min,
                           style_ibu_max, style_col_min, style_col_max,
                           style_abv_min, style_abv_max):
    """
    This method allows for data entry
    """
    c.execute("""\
                INSERT INTO styles (inputNum, name, type,
                    og_average, fg_average, ibu_average,
                    color_average, abv_average,
                    og_min, og_max, fg_min,
                    fg_max, ibu_min, ibu_max,
                    color_min, color_max,
                    abv_min, abv_max) VALUES(?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
              (number, style_name, style_type, style_og_avg, style_fg_avg,
                           style_ibu_avg, style_col_avg, style_abv_avg,
                           style_og_min, style_og_max,
                           style_fg_min, style_fg_max, style_ibu_min,
                           style_ibu_max, style_col_min, style_col_max,
                           style_abv_min, style_abv_max))
    conn.commit()

def main():
    create_table()
    url = ("https://www.brewtoad.com/styles")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    styles = soup.find("table", {"id": "styles"}).find('tbody').find_all("tr")
    k = 1
    for style in styles:
        og_avg = re.findall("\d*\.?\d+", style.text)[0]
        fg_avg = re.findall("\d*\.?\d+", style.text)[1]
        ibu_avg = re.findall("\d*\.?\d+", style.text)[2]
        col_avg = re.findall("\d*\.?\d+", style.text)[3]
        abv_avg = re.findall("\d*\.?\d+", style.text)[4]
        url_style = "https://www.brewtoad.com" + getUrl(style)
        s = requests.get(url_style)
        soup_style = BeautifulSoup(s.content, "lxml")
        stat_name = soup_style.find("header").find("h1").text
        stats = soup_style.find("ul", {"class": "stat-group-thirds"})
        list_membs = stats.find_all("li")
        for list_memb in list_membs:
            if "Type" in list_memb.text.encode('UTF-8'):
                stat_type = str(getType(list_memb))
            elif "OG" in list_memb.text.encode('UTF-8'):
                stat_og_min = getMin(list_memb, "OG")
                stat_og_max = getMax(list_memb, "OG")
            elif "FG" in list_memb.text.encode('UTF-8'):
                stat_fg_min = getMin(list_memb, "FG")
                stat_fg_max = getMax(list_memb, "FG")
            elif "IBU" in list_memb.text.encode('UTF-8'):
                stat_ibu_min = getMin(list_memb, "IBU")
                stat_ibu_max = getMax(list_memb, "IBU")
            elif "Color" in list_memb.text.encode('UTF-8'):
                stat_col = list_memb.text.encode('UTF-8').split("Color")[1]
                col_dist = [int(s) for s in stat_col.split() if s.isdigit()]
                stat_col_min = col_dist[0]
                stat_col_max = col_dist[1]
            elif "ABV" in list_memb.text.encode('UTF-8'):
                stat_abv_min = getMin(list_memb, "ABV")
                stat_abv_max = getMax(list_memb, "ABV")
        data_entry(k, stat_name, stat_type, og_avg, fg_avg,
                   ibu_avg, col_avg, abv_avg, stat_og_min, stat_og_max,
                   stat_fg_min, stat_fg_max, stat_ibu_min,
                   stat_ibu_max, stat_col_min, stat_col_max,
                   stat_abv_min, stat_abv_max)
        k = k+1
            
    c.close()
    conn.close()

# ----------------------
# Start Scraping 
# ----------------------

if __name__ == "__main__":
    main()
