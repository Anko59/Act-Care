import urllib.request as urllib2
import bs4
import unidecode
import datetime
import pygame
pygame.init()
w = pygame.display.set_mode((1400,700))
global continuer
continuer = 1
separator = ","
descritpionAuto = 0
imageAuto = 0
titreAuto = 0
salaireAuto = 0
salairesAuto = {'Garde':'1350','Journée':'650','Nuit':'700'}
repeats = {'Image':0,'Titre':0,'Salaire':0,'Description':0}
optionsPos = {'Titre':['Modifier'],'Horaires':['Garde','Journée','Nuit','Custom'],'Cadence':['Jour par Jour','Continue','Pas de Week Ends'],'Salaire':['Modifier'],'Description':['Modifier'],'Image':['Modifier'],'Format Date':['12/31/2017','31/12/2017'],'Format heure':['23:59:59'],'Ch':[]}
optionsSelec = {'Ch':'Aucun','Titre':'Modifier','Horaires':'Garde','Cadence':'Jour par Jour','Salaire':'Modifier','Description':'Modifier','Image':'Modifier','Format Date':'31/12/2017','Format heure':'23:59:59'}
def soupify(content):            
     return bs4.BeautifulSoup(content, "html.parser")
def connect(url):
    req = urllib2.Request(url)
    handle = urllib2.urlopen(req)
    the_page = handle.read().decode()
    soup = bs4.BeautifulSoup(the_page, "html.parser")
    return soup

def write(data, f, encoding = 'utf-8'):
    try:
        with open('data/' + f, 'wb') as file:
            file.write(data.encode(encoding))
    except:
        with open('data/'+normalize(f),'wb') as file:
            file.write(data.encode(encoding))

def read(f, encoding = 'utf-8'):
    with open(f, 'rb') as file:
        content = file.read()
        txt = content.decode(encoding)
    return txt
def append(data, f, encoding = 'utf-8'):
     with open(f,'ab') as file:
          file.write(data.encode(encoding))

def listToCsv(tab, s = separator):
    txt = ''
    for t in tab:
        txt += str(t) + s
    return txt

def tabToCsv(tab, s = separator):
    txt = ''
    for t in tab:
        txt += listToCsv(t, s) + '\n'
    return txt
def utf8ize(txt):
    return txt.replace('\r','').replace('\t','').encode().decode()
def normalize(txt):
    return unidecode.unidecode(txt).lower().replace(" ","").replace('\r','').replace('\n','').replace('\t','').encode().decode()

def verifiedInput(question):
    while 1:
        print(question)
        rep = input()
        verif = MCQ('Êtes-vous sûr ?',['Oui','Non'])
        if verif == 'Non': continue
        break
    return rep
def MCQ(question, options):
    opts = {}
    for i in range(len(options)):
        opts[str(i+1)] = options[i]
    rep = ''
    while rep not in opts.keys():
        print(question)
        for o in opts.keys():
            print('    ' + o + ': ' + opts[o])
        rep = input()
    return opts[rep]
        
def findChOnline():
    title = "Plus de 50 réponses trouvées."
    while title == 'Plus de 50 réponses trouvées.':
        ville = input('Ville?')
        try:
            soup = connect('https://etablissements.fhf.fr/annuaire/resultat.php?item=etablissement&cle='+ville)
            title = str(soup.find('span',attrs={'class':'nombre_res'}).find('strong').string)
            print(title)
        except: print('Pas de résultat')
    i = 0
    choix = {}

    print("Choisissez le Ch en question")
    for bloc in soup.findAll('div',attrs={'class':'bloc_groupement'}):
        choix[i] = bloc
        print(str(i) + ":" + bloc.find('h2').string.lstrip())
        i+=1
    ch = 0

    while not ch:
        try:
            ch = choix[int(input())]
        except: print('erreur, recommencez')
        

    menuLieu = ['Nom','Adresse','Ville','Code Postal','Pays','Site Web']
    adress = ch.find('span',attrs={'class':'adresse'}).string

    for x in range(len(adress.split(' '))):
        try:
            if len(adress.split(' ')[x]) == 5:
                code = int(adress.split(' ')[x])
                ville = ''
                for y in adress.split(' ')[x+1:]:
                    ville += y + ' '
                ville = ville[0:-1]
                break
        except: pass
    website = ''
    try:
        if '@' not in ch.findAll('a',attrs={'class':'link_hop'})[0].string:
            website = (ch.findAll('a',attrs={'class':'link_hop'})[0].string)
        else: print('Pas de site web disponible')
    except: print('Pas de site web disponible') 
    adress = adress.replace(str(code),'').replace(ville, '').replace(',','')
    ville = ville.capitalize()
    nouveauCh = verifiedInput('Entrez le nom du Ch ('+utf8ize(ch.find('h2').string.lstrip())+") tel qu'il apparaitra sur le site web (Ch + ville)")
    lieu = [nouveauCh,adress,ville,code,'France',website]
    txtLieu = tabToCsv([menuLieu,lieu])
    write(txtLieu,'lieu'+ville+'.csv','utf-8')
    append('\n'+nouveauCh+',,','chs.txt','ANSI')
    print('Le Fichiers lieu ' +ville+' a été crée')
    
    return nouveauCh

def findChInDatabase():
    chs = read('chs.txt','ANSI').split('\n')
    chs = [x.split(',')[0] for x in chs]
    rep = MCQ('Choisissez le Centre Hospitalier',chs)
    return rep

def findCh():
    rep = MCQ('Le Centre Hospitalier pour lequel vous voulez ajouter des missions est-il déjà sur le site ?',['Oui','Non'])

    if rep == 'Non':
        ch = findChOnline()
    elif rep == 'Oui':
        rep = MCQ("Connaissez vous le nom du Centre Hospitalier tel qu'il est enregistré sur actandcare.fr ?",['Oui','Non'])
        if rep == 'Oui':
            ch = verifiedInput('Entrez le nom du Ch')
        elif rep == 'Non':
            ch = findChInDatabase()

    return ch

def displaySelectedOptions():
    print('Options Selectionnées:')
    for opt in optionsSelec.keys():
        print("    " + opt +": " + optionsSelec[opt])

maxDays = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
class Date:
    def __init__(self,date, f = optionsSelec['Format Date']):
        if f == '12/31/2017':
            date = date.split('/')
            self.mois = int(date[0])
            self.jour = int(date[1])
            self.annee = int(date[2])
            self.separator = '/'
        elif f == '31/12/2017':
            date = date.split('/')
            self.mois = int(date[1])
            self.jour = int(date[0])
            self.annee = int(date[2])
            self.separator = '/'
        elif f == 'Custom':
            self.jour = date[0]
            self.mois = date[1]
            self.annee = date[2]
            self.separator = '/'
    def __str__(self, f = 'US'):
        if f == 'US':
            if self.jour < 10:
                jour = '0' + str(self.jour)
            else: jour = self.jour
            if self.mois < 10:
                mois = '0'+ str(self.mois)
            else: mois = self.mois
            return str(mois) + self.separator + str(jour)+ self.separator + str(self.annee)
        elif f == 'FR':
             if self.jour < 10:
                 jour = '0' + str(self.jour)
             else: jour = self.jour
             if self.mois < 10:
                 mois = '0'+ str(self.mois)
             else: mois = self.mois
             return str(jour) + self.separator + str(mois)+ self.separator + str(self.annee)
    def addJour(self,nbr = 1):
        jour = self.jour + nbr
        mois = self.mois
        annee = self.annee
        if jour > maxDays[mois]:
            jour -= maxDays[mois]
            mois += 1
            if mois > 12:
                annee += 1
                mois = 1
        return Date([jour,mois,annee],f = 'Custom')

def dateInput(t = 'Entrez une date', treat = True):
     while 1:
        print(t)
        date = input()
        if date not in keyWords.keys():
            try:
                if treat:
                     newDate = addDate(date)
                     break
                else:
                     newDate = Date(date)
                     break
            except:print('Erreur, recommencez')
        
        else:
            if date in keyWords.keys():
                newDate = date
                break
            else: print('Erreur, recommencez')
     return newDate
                             
datesDebut = []
datesFin = []
horairesDebut = []
horairesFin = []
salaires = []
descriptions = []
images = []
titres = []
def treatDate(newDate):
    global repeats, descriptionAuto, imageAuto, titreAuto, salaireAuto
    datesDebut.append(newDate)
    if optionsSelec['Horaires'] == 'Garde':
        datesFin.append(newDate)
        horaires = ['08:00:00','24:00:00']
    elif optionsSelec['Horaires'] == 'Journée':
        datesFin.append(newDate)
        horaires = ['08:30:00','18:30:00']
    elif optionsSelec['Horaires'] == 'Nuit':
        datesFin.append(newDate)
        horaires = ['20:00:00','24:00:00']
    elif optionsSelec['Horaires'] == 'Custom':
        horaires = []
        try:
             horaires.append(horaireInput('Entrez un horaire de début'))
             datesFin.append(dateInput('Entrez une date de fin', treat=False))
             horaires.append(horaireInput('Entrez un horaire de fin'))
        except Exception as e:
             print(e)
    horairesDebut.append(horaires[0])
    horairesFin.append(horaires[1])
    descriptions.append(repeats['Description'])
    images.append(repeats['Image'])
    titres.append(repeats['Titre'])
    salaires.append(repeats['Salaire'])
    
def addDate(date, dateFin = None):
    newDate = Date(date)
    if optionsSelec['Cadence'] == 'Jour par Jour':       
        treatDate(newDate)
    else:
        print('POUET')
        newDateFin = Date(dateFin)
        dateInter = newDate
        while str(newDateFin.addJour()) != str(dateInter):
            if optionsSelec['Cadence'] == 'Continue':
                treatDate(dateInter)
            elif optionsSelec['Cadence'] == 'Pas de Week Ends':
                w = datetime.date(dateInter.annee, dateInter.mois, dateInter.jour).weekday()
                if w not in ['Saturday','Sunday']:
                    treatDate(dateInter)
            dateInter = dateInter.addJour()
            
            
        
def setOptions():
    global repeats
    displaySelectedOptions()
    choix = list([x for x in optionsPos.keys()])
    choix.append('Reset Repeat')
    rep = MCQ('Quelle option voulez vous modifier ?', choix)
    if rep != 'Reset Repeat':
        rep2 = MCQ('Quel valeur voulez vous lui attribuer ?', optionsPos[rep])
        optionsSelec[rep] = rep2
    else:
        rep2 = MCQ('Quelle options voulez vous reset ?',['Description','Image','Titre','Salaire','Annuler'])
        if rep2 == 'Description': repeats['Description'] = 0
        elif rep2 == 'Image': repeats['Image'] = 0
        elif rep2 == 'Titre': repeats['Titre'] = 0
        elif rep2 == 'Salaire': repeats['Salaire'] = 0
    return 1

def descriptionInput():
    print('Entrez une description')
    return input()

def imageInput():
    print("Entrez l'url vers votre image")
    return input()

def titreInput():
    print('Entrez le titre de votre mission')
    return input()
def salaireInput():
    print('Entrez le salaire de votre mission')
    return input()
              
def horaireInput(t = 'Entrez un horaire'):
    while 1:
        print(t)
        h = input()
        x = 0
        for y in h.split(':'):
            try:
                int(y)
                x+=1
            except:
                 print('Erreur')
        if x == 3: break
        else:
            print('Erreur, recommencez')
    return h
def end():
    return 0

def cancel():
     global datesDebut, datesFin, horairesDebut, horairesFin, salaires, descriptions, images, titres 
     strDates = list([x.__str__('FR') for x in datesDebut])
     strDates.append('Annuler tout')
     print(strDates)
     rep = MCQ('Choisissez la date à supprimer',strDates)
     if rep != 'Annuler tout':
          index = strDates.index(rep)
          datesDebut.remove(datesDebut[index])
          datesFin.remove(datesFin[index])
          horairesDebut.remove(horairesDebut[index])
          horairesFin.remove(horairesFin[index])
          salaires.remove(salaires[index])
          descriptions.remove(descriptions[index])
          images.remove(images[index])
          titres.remove(titres[index])
     else:
          datesDebut = []
          datesFin = []
          horairesDebut = []
          horairesFin = []
          salaires = []
          descriptions = []
          images = []
          titres = []
     return 1
keyWords = {'options':setOptions,'o':setOptions,'fin':end,'cancel':cancel}                
def saveDataForSite(ch):
     global datesDebut, datesFin, horairesDebut, horairesFin, salaires, descriptions, images, titres 
     menuMission = ['Titre de la mission','Lieu','Date de début','Heure de début','Date de Fin','Heure de Fin','Salaire','Description','Image']
     missions = [menuMission]
     for x in range(len(titres)):
         newMission = [titres[x],ch,datesDebut[x],horairesDebut[x],datesFin[x],horairesFin[x],salaires[x],descriptions[x],images[x]]
         missions.append(newMission)
     write(tabToCsv(missions),'mission'+ch+'.csv','utf-8')
def saveDataExcel(ch):
     global datesDebut, datesFin, horairesDebut, horairesFin, salaires, descriptions, images, titres
     continuer = 1
     while continuer:
          try:
               missions = []
               for x in range(len(titres)):
                   newMission = [titres[x],ch,datesDebut[x].__str__('FR'),salaires[x],'A pourvoir']
                   missions.append(newMission)
               append(tabToCsv(missions, ';'),'Missions.csv','windows-1252')
               continuer = 0
          except:
               print("Une erreur s'est produite lors de l'enregistrement des dates dans Missions.csv.\nVérifiez que le fichier est bien fermé sur tous les ordis de la team et tapez Entrée pour réessayer")
               input()
    
def saveData():
     ch = optionsSelec['Ch']
     saveDataForSite(ch)
     saveDataExcel(ch)
