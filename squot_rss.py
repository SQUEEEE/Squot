#!/usr/bin/python

import urllib.request
import xml.etree.ElementTree as ET
import time 
from time import gmtime, strptime, strftime
import squot_irc


def UpdateRSS():
  print("Updating...")
  channel = "##tullinge"
  
  lastUpdate_file = open("lastUpdate.txt", "r")
  lastUpdate = lastUpdate_file.read() # kollar när senaste hämtningen gjordes
  lastUpdate_file.close()
  lastUpdate = strptime(lastUpdate, "%a, %d %b %Y %H:%M:%S +0000") # gör om tiden till ett jämförbart date object
  
  lastUpdate_file = open("lastUpdate.txt", "w")
  newUpdate = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) # nuvarande tid i rssfeed-form
  lastUpdate_file.write(newUpdate) # ersätter den gamla tiden för senaste hämtningen med nuvarande tid 
  lastUpdate_file.close()
  
 
  linklist_file = open("rssLinks.txt", "r") 
  linklist = linklist_file.readlines() # hämtar länkar för rssfeeds som ska kollas (lista)
  linklist_file.close()
  
  for link in linklist:
    if link.endswith("\n"):  # ta bort eventuella radbrytningar från listan
      link = link.strip()
    
    done = False
    while not done:
      try:
        rssfeed = urllib.request.urlopen(link) # öppnar länken
        rssfeedxml = rssfeed.read()
        rsscontent = ET.fromstring(rssfeedxml) 
        print("Printing something...")
        done = True
      except urllib.error.HTTPError:
        done = False
        print("Waiting...")
        time.sleep(240)
        print("Trying again...")
      
    
    items = rsscontent.find("channel").findall("item") # hittar alla items i channeln
    
    messageList = []
    
    for i in items:
      date = strptime((i.find("pubDate").text), "%a, %d %b %Y %H:%M:%S +0000") # hittar tiden i varje item (när det publicerats)
      if date > lastUpdate: # om tiden är efter senaste uppdateringen...
        messageList.append(i.find("title").text) # lägg till i listan med nya meddelanden
    
    messageList.reverse() # vänder ordningen på listan så att det senaste kommer sist 
    
    for message in messageList:
      print(message) # skriver ut varje meddelande i listan
      squot_irc.send_raw("PRIVMSG %s :%s" % (channel, message))
     