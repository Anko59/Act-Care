import urllib.request as urllib2
import bs4
import unidecode
categories = []
chs = []
base2 = 'https://etablissements.fhf.fr/annuaire/'
def connect(url):
    req = urllib2.Request(url)
    handle = urllib2.urlopen(req)
    the_page = handle.read().decode()
    soup = bs4.BeautifulSoup(the_page, "html.parser")
    return the_page, soup
def emailFinder(soup):
    departments = soup.findAll('a',attrs={'class':'nom_departement'})
    retour = ""
    for dep in departments:
        if 'affaires médicales' in dep.string.lower() or 'affaires medicales' in dep.string.lower():
            link = dep['href']
            page, soup2 = connect(base2 + link)
            try:
                "print(soup2.find('p',attrs={'class':'nom_personne'}).a.string)"
                return soup2.find('p',attrs={'class':'nom_personne'}).a.string
            except: pass
        elif 'ressources humaines' in dep.string.lower():
            link = dep['href']
            page, soup2 = connect(base2 + link)
            try:
                "print(soup2.find('p',attrs={'class':'nom_personne'}).a.string)"
                retour = soup2.find('p',attrs={'class':'nom_personne'}).a.string
            except: pass
    if retour == "":
        try:
            retour = soup.find('span',attrs={"class":"courriel"}).string
        except:pass
    return retour
class Ch:
    def __init__(self, nom, nbr,postcode = 0, services = [], mail = ""):
        self.nom = nom
        self.services = {}
        self.postcode = 0
        self.mail = ""
        self.nbr = nbr
        self.phone = 0
        self.address = ""
        chs.append(self)
    def addService(self, nom, capacite):
        if nom == 'Obstetrique': nom = 'Gynéco-obstétrique'
        nom = unidecode.unidecode(nom).lower().replace(" ","")

        self.services[nom] = capacite
        if nom not in categories:
            categories.append(nom)
    def __str__(self):
        data = [self.nom, self.postcode, self.mail,self.nbr,self.address,self.phone]
        retour = ""
        for d in data:
            retour += str(d) + ";"
        for c in categories:
            try:
                retour += self.services[c] + ";"
            except:
                retour += ";"
        return retour
baseUrl = 'https://etablissements.fhf.fr/annuaire/hopital-fiche.php?id='
nbr = 0
last = 5000
for x in range(last):
    try:
        url = baseUrl
        url+=str(x)
        the_page, soup = connect(url)
        """print(soup.head.title.string.split(" –")[0])
        print("nbr" + str(x))"""
        if "Cet établissement n'existe pas ou n'existe plus" in soup.head.title.string:
            print("NO " + str(x))
        elif "annuaire" in soup.head.title.string.lower():
            title = soup.find('header',attrs={'class':'content_header'}).h1.text
            print(title)
            if 'pital' in title.lower() and 'assoc' not in title.lower():
                try:
                    newCh = Ch(title,url)
                except: pass
                try:
                    newCh.postcode = soup.find('span',attrs={"itemprop":"postalCode"}).string
                except: pass
                try:
                    newCh.phone = soup.find('span',attrs={"itemprop":"telephone"}).string
                except: pass
                try:
                    print("poueeeeeeeet")
                    print(soup.find('span',attrs={"itemprop":"streetAddress"}).string)
                    print(soup.find('span',attrs={"itemprop":"addressLocality"}).string)
                    newCh.address = soup.find('span',attrs={"itemprop":"streetAddress"}).string + " " + soup.find('span',attrs={"itemprop":"addressLocality"}).string
                except:pass
                for s in soup.find("div",attrs={'class':'x2'}).ul.findAll('li'):
                    newCh.addService(s.text.split(':')[0], s.text.split(':')[1])
        elif "pital" in soup.head.title.string.split(" –")[0].lower():
            print("Reco")
            try:
                newCh = Ch(soup.head.title.string.split(" –")[0],url)
            except: pass
            try:
                newCh.postcode = soup.find('span',attrs={"class":"postal-code"}).string
            except: pass
            newCh.mail = emailFinder(soup)
            print(newCh.mail)
            try:
                newCh.phone = soup.find('p',attrs={'class':'standard'}).find('span',attrs={'class':'tel'}).string
                print(newCh.phone)
            except:pass
            try:
                newCh.address = soup.find('span',attrs={"class":"street-address"}).string +" "+ soup.find('span',attrs={"class":"locality"}).string
            except: pass
            try:
                services = soup.findAll('p',attrs={"class":"capacite_par_service"})
                for s in services:
                    newCh.addService(s.text.split(':')[0], s.text.split(':')[1])
            except: pass
    except: pass

txt = "Nom;Code Postal;Email;id;Adresse;Standard;"
for c in categories:
    txt += c + ";"
txt += "\n"
for ch in chs:
    txt += str(ch) + "\n"

with open('chs.csv','wb') as file:
    file.write(txt.encode('windows-1252'))
