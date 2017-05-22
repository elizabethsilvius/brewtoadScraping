import dataset
import sqlite3
from bs4 import BeautifulSoup
import requests
import re
import scrapeStyles
import scrapeYeasts
import scrapeHops
import scrapeFermentables
import scrapeExtras
import scrapeRelatedStyles
import scrapeSubstituteHops
import scrapeRecipeBasics
import scrapeRecipeYeasts
import scrapeRecipeHops
import scrapeRecipeFermentables
import scrapeRecipeExtras
import scrapeRecipeMash
import scrapeRecipeStats

# ----------------------
# SETUP  
# ----------------------

conn = sqlite3.connect('brewtoad_new.db')
conn.text_factory = str
c = conn.cursor()

# ----------------------
# Methods for Scraping
# ----------------------

def main():
    # scrape tables
    scrapeStyles.main()
    scrapeYeasts.main()
    scrapeHops.main()
    scrapeFermentables.main()
    scrapeExtras.main()
    scrapeRelatedStyles.main()
    scrapeSubstituteHops.main()
	# create tables for scraping recipes
    scrapeRecipeBasics.create_table()
    scrapeRecipeYeasts.create_table()
    scrapeRecipeHops.create_table()
    scrapeRecipeFermentables.create_table()
    scrapeRecipeExtras.create_table()
    scrapeRecipeMash.create_table()
    scrapeRecipeStats.create_table()
	# initialize table keys
    p = 1
    k = 1
    y = 1
    h = 1
    f = 1
    e = 1
    m = 1
    s = 1
	# while page numbers exist
    while p < 10347:
        url = "https://www.brewtoad.com/recipes?page=%s&sort=created_at&sort_reverse=true" % p
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        recipes = soup.find_all("li", {"class": "recipe-container"})
		# scrape basics
        for recipe in recipes:
            try:
                rec_name = scrapeRecipeBasics.getName(recipe)
                rec_style = scrapeRecipeBasics.getStyle(recipe)
                rec_og = scrapeRecipeBasics.getOG(recipe)
                rec_fg = scrapeRecipeBasics.getFG(recipe)
                rec_ibu = scrapeRecipeBasics.getIBU(recipe)
                rec_abv = scrapeRecipeBasics.getABV(recipe)
                rec_type = scrapeRecipeBasics.getType(recipe)
                scrapeRecipeBasics.data_entry(k, rec_name, rec_style, rec_og, rec_fg, rec_ibu, rec_abv, rec_type)
            except:
                pass
            rec_url = scrapeRecipeYeasts.getUrl(recipe)
            rec_name = scrapeRecipeYeasts.getName(recipe)
            page = requests.get(rec_url)
            pagesoup = BeautifulSoup(page.content, "lxml")
			# scrape yeasts
            try:   
                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'yeasts'}).find('tbody').find_all('tr')
                for line in lines:
                    rec_yeast = scrapeRecipeYeasts.getYeast(line)
                    rec_lab = scrapeRecipeYeasts.getLab(line)
                    rec_att = scrapeRecipeYeasts.getAtt(line)
                    scrapeRecipeYeasts.data_entry(y, k, rec_name, rec_yeast, rec_lab, rec_att)
                    y = y + 1
            except:
                pass
			# scrape Hops
            try:
                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'hops'}).find('tbody').find_all('tr')
                for line in lines:
                    rec_amt = scrapeRecipeHops.getAmt(line)
                    rec_hop = scrapeRecipeHops.getHop(line)
                    rec_time = scrapeRecipeHops.getTime(line)
                    rec_use = scrapeRecipeHops.getUse(line)
                    rec_form = scrapeRecipeHops.getForm(line)
                    rec_aa = scrapeRecipeHops.getAA(line)
                    scrapeRecipeHops.data_entry(h, k, rec_name, rec_amt, rec_hop, rec_time, rec_use, rec_form, rec_aa)
                    h = h + 1
            except:
                pass
			# scrape fermentables
            try:
                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'fermentables'}).find('tbody').find_all('tr')
                for line in lines:
                    rec_amt = scrapeRecipeFermentables.getAmt(line)
                    rec_ferm = scrapeRecipeFermentables.getFerm(line)
                    rec_malt = scrapeRecipeFermentables.getMalt(line)
                    rec_use = scrapeRecipeFermentables.getUse(line)
                    rec_ppg = scrapeRecipeFermentables.getPPG(line)
                    rec_col = scrapeRecipeFermentables.getCol(line)
                    scrapeRecipeFermentables.data_entry(f, k, rec_name, rec_amt, rec_ferm, rec_malt, rec_use, rec_ppg, rec_col)
                    f = f + 1
            except:
                pass
				# scrape Extras
            try:
                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'extras'}).find('tbody').find_all('tr')
                for line in lines:
                    rec_amt = scrapeRecipeExtras.getAmt(line)
                    rec_ext = scrapeRecipeExtras.getExt(line)
                    rec_time = scrapeRecipeExtras.getTime(line)
                    rec_use = scrapeRecipeExtras.getUse(line)
                    scrapeRecipeExtras.data_entry(e, k, rec_name, rec_amt, rec_ext, rec_time, rec_use)
                    e = e + 1
            except:
                pass
			# scrape mash steps
            try:
                lines = pagesoup.find('body').find('div',{'class': 'site-container recipes recipes-show'}).find('div', {'class': 'subnav'}).find('div', {'class': 'recipe-show--ingredients'}).find('table', {'id': 'mash_steps'}).find('tbody').find_all('tr')
                for line in lines:
                    rec_step = scrapeRecipeMash.getStep(line)
                    rec_heat = scrapeRecipeMash.getSource(line)
                    rec_temp = scrapeRecipeMash.getTemp(line)
                    rec_time = scrapeRecipeMash.getTime(line)
                    scrapeRecipeMash.data_entry(m, k, rec_name, rec_step, rec_heat, rec_temp, rec_time)
                    m = m + 1
            except:
                pass
			# scrape stats
            try:
                lines = pagesoup.find('body').find('div',{'class': 'soft'})
                rec_batch = scrapeRecipeStats.getBatch(lines)
                rec_boil = scrapeRecipeStats.getBoil(lines)
                rec_eff = scrapeRecipeStats.getEff(lines)
                rec_prim = scrapeRecipeStats.getPrim(lines)
                rec_sec = scrapeRecipeStats.getSec(lines)
                rec_ibu = scrapeRecipeStats.getIBU(lines)
                scrapeRecipeStats.data_entry(s, k, rec_name, rec_batch, rec_boil, rec_eff, rec_prim, rec_sec, rec_ibu)
                s = s + 1
            except:
                pass
            k = k + 1
        print p    
        p = p + 1
    c.close()
    conn.close()
    
# ----------------------
# Start Scraping 
# ----------------------
if __name__ == '__main__':
    main()

    
        


    
