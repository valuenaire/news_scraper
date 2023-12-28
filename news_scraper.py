from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd
from datetime import datetime, timezone, timedelta
from tqdm import tqdm
from summariser import summarize_in_batches
import os


data = []





def scrap_livemint():
    urls = ["https://www.livemint.com/topic/mergers-and-acquisition",
"https://www.livemint.com/topic/fund-raising",
"https://www.livemint.com/topic/investment",
"https://www.livemint.com/market",
"https://www.livemint.com/news",
"https://www.livemint.com/ai",
"https://www.livemint.com/market",
"https://www.livemint.com/economist",
"https://www.livemint.com/companies"]
    
    for baseURL in urls:
        url = baseURL
        page = 1
        loop = True
        while (loop):
            webPage = req.get(url)
            body = BS(webPage.content, "html.parser")

            for div in body.find_all("div", {"class": "listingNew"}):
                span1 = div.find("span", {"class": "fl date"})
                spans = span1.find_all("span")
                time = spans[1].text
                if "IST" in time:
                    h2 = div.find("h2")
                    title = h2.text
                    link = h2.find("a")["href"]
                    webPage = req.get("https://www.livemint.com" + link)
                    body = BS(webPage.content, "html.parser")
                    text = ""
                    for p in body.find_all("p"):
                        text += p.text
                    
                    # Generate summary
                    
                    # summary = generate_summary(text, num_sentences=3)
                  

                    data.append({"title": title, "link": "https://www.livemint.com" + link,
                                "source": "LiveMint", "time": time, 
                                "text":text})
                    
                else:
                    loop = False
                    break

            page = page+1

            url = baseURL + "/page-" + str(page)
          


def scrap_businessToday():
    urls =["https://www.businesstoday.in/latest/corporate"
"https://www.businesstoday.in/entrepreneurship/startup-fundraising"]
    for baseURL in urls:
        url = baseURL
        webPage = req.get(url)

        body = BS(webPage.content, "html.parser")

        current_date = datetime.now().strftime("%b %d, %Y")
        for div in body.find_all("div", {"class": "widget-listing"}):

            time = div.find("span").text
            if current_date in time:
                a = div.find("h2").find("a")
                title = a.text
                link = a["href"]
                webPage = req.get(link)
                body = BS(webPage.content, "html.parser")
                text = ""
                for p in body.find_all("p"):
                    text += p.text

               
                data.append({"title": title,
                            "link": link, "source": "Business Today", "time": time,"text":text})
              
            else:
                break
      


def scrap_moneyControl():
    urls = ["https://www.moneycontrol.com/news/business/",
"https://www.moneycontrol.com/news/markets/",
"https://www.moneycontrol.com/news/companies/",
"https://www.moneycontrol.com/news/business/companies/",
"https://www.moneycontrol.com/news/business/mergers-acquisitions/",
"https://www.moneycontrol.com/news/tags/fund-raising.html",
"https://www.moneycontrol.com/news/business/ipo/",
"https://www.moneycontrol.com/news/business/stocks/"
    ]

    for baseUrl in urls:
        url = baseUrl
        page = 1
        loop = True
        while (loop):
            webPage = req.get(url)
            body = BS(webPage.content, "html.parser")
            current_timestamp = datetime.now(
                timezone(timedelta(hours=5, minutes=30))).strftime("%B %d")
            for div in body.find_all("li", {"class": "clearfix"}):
                time = div.find("span").text
                if current_timestamp in time:
                    a = div.find("h2").find("a")
                    title = a.text
                    link = a["href"]
                    webPage = req.get(link)
                    body = BS(webPage.content, "html.parser")
                    text = ""
                    for p in body.find_all("p"):
                        text += p.text
                    
                  

                    data.append({"title": title,
                                "link": link, "source": "Money Control", "time": time, "text":text})
                    
                   
                else:
                    loop = False
                    break
            page = page+1
            url = baseUrl + "page-" + str(page)
          

def scrap_vccircle():
    catagories = ['venture-capital', 'pe', 'm-a']
    for catagory in catagories:
        baseurl = "https://www.vccircle.com/deal-type" + f"/{catagory}"
        url = baseurl
        webPage = req.get(url)
        body = BS(webPage.content, "html.parser")
        current_timestamp = datetime.now().strftime("%d %B")
        loop = True
        page = 1


        while loop:
            for div in body.find_all("div", {"class": "listingPage_article-list__EecoW"}):
                time = div.find("div", {"class": "newsCard_date__AxIUu"}).text
               
                if current_timestamp in time:
                    a = div.find("h4").find("a")
                    title = a.text
                    link = a["href"]
                    webPage = req.get(f"https://www.vccircle.com/{link}")
                    body = BS(webPage.content, "html.parser")
                    text = ""
                    for p in body.find_all("p"):
                        text += p.text
                  
                    data.append({"title": title,
                                "link": f"https://www.vccircle.com/{link}", "source": "vccircle", "time": time, "text":text})
                    
                    
                else:
                    loop = False
                    break

            page += 1
            url = baseurl + f"/all/{page}"

def scrap_ft():
    url = "https://www.ft.com/mergers-acquisitions"
    webPage = req.get(url)
    body = BS(webPage.content, "html.parser")
    timestamp = datetime.now(timezone.utc).strftime("%d %B, %Y").lstrip('0')
    for li in body.find_all("li", {"class": "o-teaser-collection__item"}):
        time = li.find("time")
        div= li.find("div", {"class": "o-teaser__heading"})
        if time is None:
            continue
        if timestamp not in time.text:
            break
        title = div.find("a").text
        link = div.find("a")["href"]
        webPage = req.get("https://www.ft.com" +link)
        body = BS(webPage.content, "html.parser")
        text = ""
        for p in body.find_all("p"):
            text += p.text
        
        data.append({"title": title, "link": "https://www.ft.com" +link,
                    "source": "Financial Times", "time": time.text, "text":text})
       
 

def scrap_reuters():
    url = "https://www.reuters.com/tags/mergers-acquisitions/"
    webPage = req.get(url)
    body = BS(webPage.content, "html.parser")
  
    for div in body.find_all("li"):
        time = div.find("time")
        title = div.find("h3").text
        link = title.find("a")["href"]
        webPage = req.get("https://www.reuters.com" +link)
        body = BS(webPage.content, "html.parser")
        text = ""
        for p in body.find_all("p"):
            text += p.text
        data.append({"title": title, "link": "https://www.reuters.com" +link,
                    "source": "Reuters", "time": time.text, "text":text})
        
 




scraping_functions = [
    scrap_livemint,
    scrap_businessToday,
    scrap_moneyControl,
    scrap_vccircle,
    scrap_ft,
    scrap_reuters  # Add this if you want to include Reuters in your scraping process.
]


# Total number of functions to scrape
total_sites = len(scraping_functions)

# Initialize tqdm progress bar
with tqdm(total=total_sites, desc="Scraping Websites", unit="site") as pbar:
    for scrape_func in scraping_functions:
        scrape_func()
        pbar.update(1)  # Update progress after each site is scraped

# Create a dataframe from the scraped data
df = pd.DataFrame(data)


news_articles = df['text']

# Summarize articles
summarized_articles = summarize_in_batches(news_articles, batch_size=2, max_length=300, min_length=100)

# Add the summaries to the dataframe
df['summary'] = summarized_articles

# save the dataframe as a csv file with the current date and time as the file name
name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# create directory if it doesn't exist
if not os.path.exists("data"):
    os.mkdir("data")

# save the dataframe as a csv file with the current date and time as the file name

df.to_csv(f"data/{name}.csv", index=False)


   




