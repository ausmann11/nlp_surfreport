from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time as timez

report_df=pd.DataFrame(columns=['date','part_of_day','time','size','surface','temp','wind','high','low','rise',
                                'sunset','text'])

for x in range(10,30):
    url="http://wblivesurf.com/reports/c-street-{}".format(x)
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html.parser')
    '''
    error=soup.find('h2').text
    skip='Error 404 - Page Not Found'
    if error == skip:
        continue
    '''
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

    report_dict={'date':date[0],'part_of_day':when[0],'time':time[0],'size':size,'surface':surface,'temp':temp,
                'wind':wind,'high':high,'low':low,'rise':rise,'sunset':sunset,'text':text}


    temp_df=pd.DataFrame(report_dict)#,index=[0])

    report_df=report_df.append(temp_df)

    timez.sleep(20)



report_df.reset_index(inplace=True,drop=True)
len(report_df)
report_df
