from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

report_df=pd.DataFrame(columns=['date','part_of_day','time','size','surface','temp','wind','high','low','rise',
                                'sunset','text'])

for x in range(10):
    url="http://wblivesurf.com/reports/c-street-"+str(10+x)
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html.parser')

    conditions={}
    for strong_tag in soup.find_all('strong'):
        conditions.update({strong_tag.text:strong_tag.next_sibling})

    size=conditions['Swell Size:'].lstrip()
    surface=conditions['Water Surface:'].lstrip()
    temp=conditions['Water Temp:'].lstrip()
    wind=conditions['Wind:'].lstrip()
    high=conditions['High Tide:'].lstrip()
    low=conditions['Low Tide:'].lstrip()
    rise=conditions['Sunrise:'].lstrip()
    sunset=conditions['Sunset:'].lstrip()

    report=soup.find('div',attrs={'class':'entry-content'})
    report=str(report)

    pattern=r"\"(\d*\:\d.+?)\""
    time=re.findall(pattern,report)

    pattern=r"\"(\d\d\d\d\-\d.\-\d.?)T"
    date=re.findall(pattern,report)

    pattern=r"g\>([a-zA-Z].+)\:"
    when=re.findall(pattern,report)

    pattern="g\>.+g\>([a-zA-Z].+)\</"
    text=re.findall(pattern,report)

    report_dict={'date':date,'part_of_day':when[0],'time':time,'size':size,'surface':surface,'temp':temp,'wind':wind,
             'high':high,'low':low,'rise':rise,'sunset':sunset,'text':text}


    temp_df=pd.DataFrame(report_dict)

    report_df.append(temp_df)



report_df
