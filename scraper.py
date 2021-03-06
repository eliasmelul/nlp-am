import pandas as pd
import requests
from bs4 import BeautifulSoup
import locale
from datetime import datetime

def initiate_scraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    return headers
    
headers = initiate_scraper()

def get_seeallreviews_link(url):
    seeallreviews_HTML = requests.get(url=url)
    seeall_soup = BeautifulSoup(seeallreviews_HTML.content, features = 'lxml')
    seeallreviews_link = seeall_soup.find_all("a", {"data-hook":"see-all-reviews-link-foot"})
    try:
        seeallreviews_link = seeallreviews_link[0].get('href')
        domain = 'https://www.amazon.com'
        seeallreviews_link = str(domain) + str(seeallreviews_link)
    except:
        seeallreviews_link = print("Hmmm... seems like Amazon has blocked the IP... Sorry about that! Hope you come back later (:")
    return seeallreviews_link
    print(seeallreviews_link)
    
def get_numberofreviews(seeallreviews_link):
    # Get the HTML code for the first page (not the 'see all reviews site')
    firstpage_HTML = requests.get(seeallreviews_link, headers = headers)
    # Create a soup from HTML
    firstpage_soup = BeautifulSoup(firstpage_HTML.content, features = 'lxml')
    # Find chunk of code that includes total number of customer reviews
    # Get text, which includes the number of customer reviews
    numrev_subsoup = firstpage_soup("div", {'data-hook':'total-review-count'})
    numrev_text = numrev_subsoup[0].get_text()
    
    numrev = str(numrev_text)
    # There are 18 characters in the string ' customer ratings', so we can backwards slice to get the number and then raplace any commas with nothing
    numberof_reviews = numrev.strip()[:-18]
    numberof_reviews = numberof_reviews.replace(',','')
    return numberof_reviews
    
def get_numberof_pages(numberof_reviews):
    n = (round(float(numberof_reviews)/10,0))-3
    return n
 
def get_soup(page_link):
    response_page = requests.get(page_link, headers = headers)
    soup_page = BeautifulSoup(response_page.content, features = 'lxml')
    return soup_page
    
def get_next_page(current_soup):
    domain = 'https://www.amazon.com'
    paging_link = current_soup.find_all("li", {'class':'a-last'})
    paging_link = paging_link[0].find("a")['href']
    paging_link = str(domain) + str(paging_link)
    return paging_link
    
def get_page_reviews(page_soup):
    page_reviews = page_soup.find_all("div", {'data-hook':'review'}) # create soup of first page
    page_reviews_df = pd.DataFrame()
    for i in range(10):
        page_reviewsi = page_reviews[i]
        name = page_reviewsi.find_all("span", {'class':'a-profile-name'})[0].get_text()
        date = page_reviewsi.find_all("span", {'data-hook':'review-date'})[0].get_text()
        date = date[33:]
        date = datetime.strptime(str(date), "%B %d, %Y")
        stars = page_reviewsi.find_all("a", {'class':'a-link-normal'})[0].get_text()
        titlerev = page_reviewsi.find_all("a", {'data-hook':'review-title'})[0].get_text(strip=True)
        review_body = page_reviewsi.find_all("span", {'data-hook':'review-body'})[0].get_text(strip=True)
        try:
            helpful = page_reviewsi.find_all("span", {'data-hook':'helpful-vote-statement'})[0].get_text()
            helpful = helpful[:-26]
        except:
            helpful = '0 people found this helpful'
        row_df = pd.DataFrame({'name':[name], 'date': [date], 'stars': [stars], 'title':[titlerev], 'review_body':[review_body], 'helpful':[helpful]})
        page_reviews_df = page_reviews_df.append(row_df)
        page_reviews_df = pd.DataFrame(page_reviews_df)
    return page_reviews_df

def get_all_reviews(first_page_link, total_pages):
    urls_list = []
    all_reviews = pd.DataFrame()
    domain = 'https://www.amazon.com'
    
    soup_pagei = get_soup(first_page_link)
        
    for i in range(min(int(total_pages), 499)):
        try:
            
            page_reviews_df = get_page_reviews(soup_pagei)
        
            urls_list.append(first_page_link)
        
            all_reviews = all_reviews.append(page_reviews_df, ignore_index = True)

            first_page_link = get_next_page(soup_pagei)
        
            soup_pagei = get_soup(first_page_link)
        except:
            break
        print(i)
    return all_reviews
   
def get_dataframe(url):
    headers = initiate_scraper()
    try:
        seeallreviews_link = get_seeallreviews_link(url)
    except:
        seeallreviews_link = url
        pass
    numberof_reviews = get_numberofreviews(seeallreviews_link)
    numberof_pages = get_numberof_pages(numberof_reviews)
    page_reviews = get_all_reviews(seeallreviews_link, numberof_pages-2)
    return page_reviews

 # Try it yourself!:
url =  'https://www.amazon.com/gp/product/B07Z8BMLY8?pf_rd_r=TSWM40DT3THWKKJKY6S3&pf_rd_p=ab873d20-a0ca-439b-ac45-cd78f07a84d8&th=1'
page_reviews = get_dataframe(url)
page_reviews