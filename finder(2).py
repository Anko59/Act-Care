import urllib.request as urllib2
import bs4
import unidecode
mails = []
spes = ['urgentiste','anesthesiste','psychiatre','chirurgien','geriatre','medecin','generaliste','docteur','dr.','reanimateur','neurologue','nefrologue','cardiologue','enterologue','gynecologue']
"""spes = ['urgentiste','anesthesiste','docteur','dr.']"""
separator = ";"
def normalize(txt):
    return unidecode.unidecode(txt).lower().replace(" ","").replace('\r','').replace('\n','').replace('\t','').encode().decode()

def beautify(txt):
    return txt.lower().replace('\r','').replace('\n','||').replace('\t','').encode().decode().capitalize()

flattenMails = []
def connect(url):
    print(url)
    req = urllib2.Request(url)
    handle = urllib2.urlopen(req)
    the_page = handle.read()
    soup = bs4.BeautifulSoup(the_page, "html.parser")
    return soup
def listToCsv(tab):
    txt = ''
    for t in tab:
        txt += str(t) + separator
    return txt

def tabToCsv(tab):
    txt = ''
    for t in tab:
        txt += listToCsv(t) + '\n'
    return txt
def findUrls(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links
def findMails(soup,c):
    global mails
    text = soup.get_text()
    for x in spes:
        print(x)
        if (x in text):
            mails.append([beautify(text[text.index(x)-20:text.index(x)+20]), c])
            print('YEAH' + beautify(text[text.index(x)-20:text.index(x)+20]))
    for line in text.split('\n'):
        for line in line.split(' '):
            if '@' in line and ('.fr' in line or '.com' in line) and len(line) < 50 and (normalize(line) not in flattenMails):
                print(line)
                mails.append([normalize(line),c])
                flattenMails.append(normalize(line))
                
                
    return mails
with open('chs.csv','rb') as file:
    txt = file.read().decode('windows-1252')
    content = {}
    for line in txt.split('\n')[100:150]:
        line = line.split(';')
        try:
            content[line[0]] = line[3]
        except: pass

y = list(content.keys())
for k in y:
    try:
        c = content[k] 
        soup = connect(c)
        if '@' not in soup.findAll('a',attrs={'class':'link_hop'})[0].string:
            content[k] = (soup.findAll('a',attrs={'class':'link_hop'})[0].string)
        else:
            del content[k]
    except: del content[k]

chs = {}
errors = []
visitedUrls = []
for c in content.keys():
    try:
        chs[content[c]] = content[c][12:]
        soup = connect(content[c])
        findMails(soup, c)
        for url in findUrls(soup):
            if url[0] == '/':
                url = content[c] + url
            if url not in visitedUrls:
                visitedUrls.append(url)
                soup2 = connect(url)
                mails += findMails(soup2, c)
    except Exception as e: print(str(e))

txt = tabToCsv(mails)
with open('mails.csv','wb') as file:
    file.write(txt.encode('windows-1252'))
