# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 16:04:29 2019

@author: Federico
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

Info1=["Giovanna", "Mario", "Giulia", "Carlo"]

Info2=["giovanna@gmail.com", "mario@inwind.it","giulia@yahoo.com","carlo@hotmail.com"]

#it send the an email to multiple receivers, stated in the Info2 List

sender_email = "sender@gmail.com"#
#receiver_email = " "
#password = input("Type your password and press enter:")
password = "sender's password"

for i in range (0, len(Info1)):
    receiver_email= Info2[i]
    message = MIMEMultipart("alternative")
    message["Subject"] = "Presentation of NanoCuvette™"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    
    # Create the plain-text and HTML version of your message
    #text = """\Hey"""
    
    # it also injects the content of the Info1 List in the messagge, to address someone personally
    
    html = """\
    <html>
      <body>
        <p>Dear Prof.{code}<br>
           I send you this mail on behalf of the company XYZ.<br>
           XYZ is a young company which produces brooms<br> 
           Due to its unique characteristics, brooms are an ideal product for the following tasks:<br>
           Best regards,<br>
           Federico Masini<br>
        </p>
      </body>
    </html>
    """.format(code=Info1[i])
    
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