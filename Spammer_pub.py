# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 12:26:00 2019

@author: Federico
"""

#Scrapes a websites for any tables, sorting the relevant data (ex: names, tlf numbers, titles) 
#and emails, creating a compact dataset, then uses the data to send emails

from bs4 import BeautifulSoup
import requests
import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

source = requests.get('http://www.chem.ed.ac.uk/staff/academic-staff').text
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

"""    
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
"""

sender_email = "sender's email"#

#receiver_email = "receiver's mail"
password = input("Type your password and press enter:")
#password = "password"


for i in range (0, len(Data)):
    receiver_email= Mail[i]
    message = MIMEMultipart("alternative")
    message["Subject"] = "Presentation of NanoCuvette™"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    
    # Create the plain-text and HTML version of your message
    #text = """\Hey"""
    
    
    html = """\
    <html>
      <body>
        <p>Dear {code}<br>
           I send you this mail on behalf of the company.<br>
           Furthermore, the company provides in-cloud data processing and storing: the software is user-friendly,<br>
           fast and hosted by, which ensures that the customers data is handled reliably,<br>
           privately and securely.<br>
           If this could be interesting for you, I would love to meet you <br> 
           (or whoever in your company/department could be interested in the product)<br> 
           at your convenience, to showcase the product capability and discuss possible purchase.<br>
           Best regards,<br>
           FM<br>
        </p>
      </body>
    </html>
    """.format(code=Information1[i])
    
    # Turn these into plain/html MIMEText objects
   # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
   # message.attach(part1)
    message.attach(part2)
    
    # Creates secure connection with server and sends email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                    sender_email, receiver_email, message.as_string()
                    )
            print ('email sent')
    except:
        print ('error sending email')
        
print('task completed')

