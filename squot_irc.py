#!/usr/bin/python

import sys
import socket
import string
import squot_rss

def connect(HOST, PORT, NICK, IDENT, REALNAME, CHAN):
  global s, s_file
  s=socket.socket()
  s_file = s.makefile("rwb") # använd en fil-instans för att få tillgång till readline()
  s.connect((HOST, PORT))
  send_raw("NICK %s"            % NICK)
  send_raw("USER %s %s bla :%s" % (IDENT, HOST, REALNAME))
  send_raw("JOIN :%s"           % CHAN)

def send_raw(msg): # hjälpfunktion för att slippa skicka radbrytning manuellt varje gång. dessutom ser vi tack vare print() vad som skickas
  print("<", msg)
  s.send(bytes(msg, "utf-8")) # se till att skicka bytes, inte str
  s.send(b"\r\n") # skicka radbrytning för att avsluta kommandot (viktigt!)

def maintain():
  while True:
    line = s_file.readline() # använd fil-instansen istället för socketen; läs en rad som servern skickar
    line = line.rstrip() # ta bort \r\n i slutet av raden (rstrip = "right strip");
    try:
      line = line.decode("utf-8")
    except UnicodeDecodeError:
      line = line.decode("latin_1")
					# anta UTF-8 vid konvertering till str från bytes (det är säkert korkat)
    #print(">", line)


    line_args = line.split(" ") # dela på mellanslag
    if line_args[0] == "PING": # om första ordet på raden är PING...
      send_raw("PONG %s" % line_args[1]) # skicka tillbaka PONG med det andra ordet på raden
    
    elif line[0] == ":": # om raden börjar på ":"... (kolla på outputen från servern för att se vilka sorts rader som gör det)
      tmp = line[1:].split(" :", 1) # dela på " :", titta på formatet på vad servern skickar för att förstå varför. vi anger 1 som "maxsplit" för
				    # att se till att inte splitta på annat än den första " :" även om det finns flera " :".
				    # line[1:] används för att "skära bort" ":" i början av raden
      line_args = tmp[0].split(" ") # dela allt INNAN " :" på mellanslag
      if len(tmp) > 1: line_args.append(tmp[1]) # och sätt ihop allt som delades på mellanslag med allting efter " :" (om det finns)
      print(line_args) # spamma ut arrayerna direkt efter att vi skriver ut det som servern skickar direkt, som jämförelse
      # här kan man kolla om line_args innehåller ett kommando från servern.(index 1)