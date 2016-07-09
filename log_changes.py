#!/usr/bin/env python
# you need
# pip install requests requests_cache lxml

def parse():
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
      rank = int(tree.findall(".//country")[0].attrib["rank"])
      #rank = int(tree.findall(".//popularity")[0].attrib["text"])
      c.execute('insert into pages values (?, ?)', [url, rank])
    except:
      import sys
      print "Unexpected error:", sys.exc_info()[0]
      print uu
      print url
      raise

  headers = ['dato']
  from datetime import datetime
  d = datetime.today()
  data = ['%d-%02d-%02d' % (d.year, d.month, d.day)]
  for row in c.execute('select url, rank from pages order by url asc'):
    headers.append(row[0])
    data.append(str(row[1]))

  print "\t".join(headers)
  print "\t".join(data)
  
if __name__ == "__main__":
  parse()

