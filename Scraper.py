#Scrapes a websites for any tables, sorting the relevant data (ex: names, tlf numbers, titles) 
#and emails, creating a compact dataset

from bs4 import BeautifulSoup
import requests
import pandas as pd

source = requests.get('https://www.nottingham.ac.uk/chemistry/people/index.aspx').text
soup = BeautifulSoup(source, 'lxml')
#print(soup)

replaceString = "" # replace each \n tag with ""
cleansoup = BeautifulSoup(str(soup).replace("\n", replaceString),'lxml')

#imported_table=cleansoup.find('table',{'class':'wikitable sortable'}) #only works for wikipedia!
imported_table=cleansoup.find('table')
#print(imported_table)



headers = imported_table.find_all('th')
datas = imported_table.find_all('tr')
email = imported_table.select('a[href^=mailto]')


Mail=[]

for i in email:
    href=i['href']
    try:
        str1, str2 = href.split(':')
    except ValueError:
        break
        
    Mail.append(str2)


Data=[]

for tr in datas:
    td=tr.find_all('td')
    row=[i.text for i in td]
    Data.append(row)
    #print(row)

Data = [x for x in Data if x] #gets rid of everything that is empty in the Data list
 
Mail = [x for x in Mail if x]    


# creates separate lists from a list of lists

dummy=len(Data)

Information1=[]
for i in range(0,dummy):
    Information1.append(Data[i][0])
  
Information2=[]
for i in range(0,dummy):
    Information2.append(Data[i][1])  
    
Information3=[]
for i in range(0,dummy):
    Information3.append(Data[i][2]) 
    
Information4=[]
for i in range(0,dummy):
    Information4.append(Data[i][3]) 
      
    
#create a single dataframe by concatanating previously created dataframes
df1=pd.DataFrame() 
df1["Name"]= Information1
df2=pd.DataFrame() 
df2["Number"] = Information2
df3=pd.DataFrame() 
df3["Department"] = Information3
df4=pd.DataFrame() 
df4["Extra"] = Information4
df5=pd.DataFrame()
df5["E-Mail"] = Mail
result = pd.concat([df1, df2, df3, df4, df5], axis=1, sort=False)




