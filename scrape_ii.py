from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

report_df=pd.DataFrame(columns=['date','part_of_day','time','size','surface','temp','wind','high','low','rise',
                                'sunset','text'])

report_time=['sunrise-report-','mid-morning-update-','lunchtime-update-','afternoon-update-']

for i in report_time:
    for x in range(10,20):
        url="http://wblivesurf.com/reports/{}{}/".format(i,x)
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
            conditions.update({strong_tag.text : strong_tag.next_sibling})

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

        pattern=r"s\/([a-z].+)\-[r|u]"
        when=re.findall(pattern,report)

        pattern="<p>([a-zA-z].+)<"
        text=re.findall(pattern,report)

        report_dict={'date':date,'part_of_day':when,'time':time,'size':size,'surface':surface,'temp':temp,'wind':wind,
                     'high':high,'low':low,'rise':rise,'sunset':sunset,'text':text}

        temp_df=pd.DataFrame(report_dict)

        report_df=report_df.append(temp_df)

report_df.reset_index(inplace=True,drop=True)
len(report_df)
report_df.head(1)

report_df.part_of_day.value_counts()
len(report_df[report_df['part_of_day']=='sunrise'])
