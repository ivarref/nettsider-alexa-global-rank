#!/usr/bin/python
# you need
# pip install requests requests_cache lxml

def parse(url):
  import hashlib
  import requests
  from lxml import html
  import re
  import requests_cache
  requests_cache.install_cache('demo_cache')

  import sqlite3
  conn = sqlite3.connect(':memory:')
  c = conn.cursor()
  c.execute('''CREATE TABLE pages (url text, rank number)''')

  import codecs
  f = codecs.open('pages.txt', 'r', 'UTF-8')
  for url in f:
    url = url.strip()
    if url.strip() == '' or url.strip()[0] == '#':
      continue
    uu = 'http://data.alexa.com/data?cli=10&url=http://www.' + url
    page = requests.get(uu)
    tree = html.fromstring(page.content)
    try:
      #rank = int(tree.findall(".//country")[0].attrib["rank"])
      rank = int(tree.findall(".//popularity")[0].attrib["text"])
      c.execute('insert into pages values (?, ?)', [url, rank])
    except:
      import sys
      print "Unexpected error:", sys.exc_info()[0]
      print uu
      print url
      #raise

  print ""
  print ""
  print ""
  print "%s %s" % ("Nettside".ljust(21), "Global page rank (alexa.com)".rjust(10))
  for row in c.execute('select url, rank from pages order by rank asc'):
    chunks = [""]
    rank = str(row[1])
    for c in rank[::-1]:
      if len(chunks[-1]) == 3:
        chunks.append("")
      chunks[-1] += c
    
    chunks = [x[::-1] for x in chunks]
    chunks.reverse()
    print "%s %s" % (row[0].ljust(21), " ".join(chunks).rjust(10))

  
if __name__ == "__main__":
  url = 'http://data.alexa.com/data?cli=10&url=http://www.steigan.no'
  parse(url)

