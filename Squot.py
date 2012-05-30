#!/usr/bin/python

# som det helst ska funka: två trådar

import threading
import squot_irc
import squot_rss
import time

thread = threading.Thread()

squot_irc.connect("irc.freenode.net", 6667, "Squot", "aoeu", "SQUEEEE", "#tullinge-lan")

def run():
 squot_irc.maintain()
    
thread.run = run
thread.start()

while True:
  squot_rss.UpdateRSS()
  time.sleep(120)