from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler, HTTPServer

# Url Crawling Section
url = "https://time.com" #Url to Crawl
page = urlopen(url)
html_bytes = page.read()
res = []

# Function to Segregate the complete webpage from Required Data
def search(html):
    s, e = 0, 0
    while True:
        s = html.find('''li class="latest-stories__item"'''.encode(), e)
        if s == -1:
            break
        e = html.find('</a>'.encode(), s)
        res.append(
            html[s+len('''<li class="latest-stories__item"><a href="'''):e])

    return res

search(html_bytes)

# Storing Links and Titles from The Seperated and Required HTML
links = []
titles = []
for x in res:
  HREF = '''a href="'''.encode()
  indS, indE = 0, 0
  link = x
  indS = link.find(HREF)
  indE = link.find('''">'''.encode())
  url_form = '''"https://time.com/'''.encode() + link[indS+len(HREF):indE] + '''"'''.encode()
  links.append(url_form.decode('utf-8'))
  HEAD = '''<h3 class="latest-stories__item-headline">'''.encode()
  link = x
  indS = link.find(HEAD)
  indE = link.find('''</h3>\n'''.encode())
  titles.append(link[indS+len(HEAD):indE])

final = []
for i in range(6):
  obj = {"title": titles[i], "link": links[i]}
  final.append(obj)
  


# Server Variables and Functions
port = 80
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET request
    def do_GET(self):
        if self.path == '/getTimeStories':
            self.do_DATA()

    def do_DATA(self):
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write(bytes(str(final).encode()))

server = HTTPServer(('', port), myHandler)
server.serve_forever()
