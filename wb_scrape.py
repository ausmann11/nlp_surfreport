#package imports
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def scrape_wb(url):
    '''
    This function scraps WBlive and pulls in the current conditions and the written surf report.
    It converts all of the relevent data to a dataframe that is appended onto the reports.csv
    '''
#pulling in WBLive html
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html.parser')

#get conditions values from website
    conditions={}

    for strong_tag in soup.find_all('strong'):
        conditions.update({strong_tag.text : strong_tag.next_sibling})

#stripping leading space from condition values
    author=list(conditions.keys())[3]
    size=conditions['Swell Size:'].lstrip()
    surface=conditions['Water Surface:'].lstrip()
    temp=conditions['Water Temp:'].lstrip()
    wind=conditions['Wind:'].lstrip()
    high=conditions['High Tide:'].lstrip()
    low=conditions['Low Tide:'].lstrip()
    rise=conditions['Sunrise:'].lstrip()
    sunset=conditions['Sunset:'].lstrip()

#getting the written report
    report=soup.find('div',attrs={'id':'wbMainReport'}).text

    pattern=r"(\d..\d..\d.)"
    date=re.findall(pattern,report)
    date=date[0]
    
    pattern=r"\d([a-zA-z].+?)\d"
    when=re.findall(pattern,report)
    when=when[0]
    
    pattern=r"[a-z](\d*\:.....)"
    time=re.findall(pattern,report)
    time=time[0]
    
    pattern=r"([a-zA-Z].+?)\s.+"
    author=re.findall(pattern,author)
    author=author[0]
    
    pattern=r"[o][p](\w.+)"
    text=re.findall(pattern,report)
    text=text[0]
    
#putting all the values into a dictionary
    report_dict={'date':date,'part_of_day':when,'time':time,'author':author,'size':size,
                 'surface':surface,'temp':temp,'wind':wind,'high':high,'low':low,'rise':rise,
                 'sunset':sunset,'text':text}

#dict to df
    report_df=pd.DataFrame(report_dict,index=[0])
    
    return report_df
#append new df rows to csv
    #report_df.to_csv(r'/home/pi/Documents/Surf project/reports',mode='a',header=False)
    


url="http://wblivesurf.com"
df=scrape_wb(url)

