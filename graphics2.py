import pygame
from pygame.locals import *
from math import *
from functions import *
from random import randrange
from online import *
pygame.init()
pygame.scrap.init()
w = pygame.display.set_mode((1400,700))
rect = pygame.draw.rect
flip = pygame.display.flip
clickableObjects = []
hitableObjects = []
shownObjects = []
maj = False
def writeW(text, pos, size = 17, color = (0,0,0), t = 0):
     if t == 0:
         texte = pygame.font.Font(None,size).render(text,0,color)
     w.blit(texte,pos)

def void(obj = None):
    pass


class Widget:
    def __init__(self, pos, d, clickedFunc = void, unclickedFunc = void, listenToClicks = False, listenToKeys = False, shown = True, hitFunc = void, parent = None, children = []):
        self.pos = pos
        self.dim = d
        self.clickedFunc = clickedFunc
        self.unclickedFunc = unclickedFunc
        self.clicked = False
        self.hitFunc = hitFunc
        self.children = children
        self.setParent(parent)
        self.listenToClicks = listenToClicks
        self.listenToKeys = listenToKeys
        
        if shown: self.show()
    def show(self, showchildren = True):
        if self not in shownObjects:
            shownObjects.append(self)
        if self.listenToKeys and self not in hitableObjects:
            hitableObjects.append(self)
        if self.listenToClicks and self not in clickableObjects:
            clickableObjects.append(self)
        if showchildren:
            for c in self.children:
                c.show()
    def hide(self, hideChildren = True):
        if self in shownObjects:
            shownObjects.remove(self)
        if hideChildren:
            for c in self.children:
                c.hide()
        cleanListeners()
    def setParent(self, parent):
        self.parent = parent
        #if parent != None and self not in parent.children:
            #parent.children.append(self)
            #pass

        

class DropDownList(Widget):
    def textClicked(text):
        text.clicked = True
        text.parent.value = text.text
        text.parent.parent.callBack(text.text)
    def textUnclicked(text):
        text.clicked = False
        if text.parent.value == text.text:
            text.parent.value = None
    def __init__(self, pos, opts, parent = None, size = 20, shown = False, clickedFunc = void):
        x = pos[0] + 3
        y = pos[1] + 5
        textes = []
        for o in opts:
            newText = Texte(o, [x,y],size = size, clickedFunc = DropDownList.textClicked, unclickedFunc = DropDownList.textUnclicked, parent = self, shown = shown)
            textes.append(newText)
            y += (size + 2)
        try:
            l = max(list([len(o) for o in opts])) * (size / 2) + 10
        except: l = 50
        h = len(opts) * (size + 2) + 5
        Widget.__init__(self,pos,[l,h], shown = shown, parent = parent, children = textes, unclickedFunc = self.unclickedFunc, listenToClicks = True)
        self.value = None
        self.opts = opts
        self.size = size
    def unclickedFunc(self, b = None):
        if self.parent == None or self.parent.clicked == False:
            self.hide()
    def draw(self):
        rect(w, (0,0,0), self.pos + self.dim, 3)
        rect(w, (255,255,255), self.pos + self.dim) 

        
class DateEntry(Widget):
    touches = {K_0:0,K_1:1,K_2:2,K_3:3,K_4:4,K_5:5,K_6:6,K_7:7,K_8:8,K_9:9,K_KP0:0,K_KP1:1,K_KP2:2,K_KP3:3,K_KP4:4,K_KP5:5,K_KP6:6,K_KP7:7,K_KP8:8,K_KP9:9,46:'/',267:'/'}
    def __init__(self,pos, d = [450,30], content = '', size = 23, title = 'Entrez une date à ajouter', mate = None):
        Widget.__init__(self, pos, d, clickedFunc = self.isClicked, unclickedFunc = self.isNotClicked, listenToClicks = True, hitFunc = self.isHit)
        self.content = content
        self.size = size
        self.baseColor = (0,0,0)
        self.usedColor = self.baseColor
        self.title = title
        self.text = Texte(title,[pos[0], pos[1] - 20])
        self.subText = Texte('',[pos[0], pos[1] + 40], color = (255,0,0), shown = False)
        self.mate = mate
    def draw(self):
        rect(w, self.usedColor, self.pos + self.dim, 5)
        w.blit(pygame.font.Font(None,self.size).render(self.content,1,(0,0,0)), [self.pos[0]+10, self.pos[1] + 8])
    def isHit(self, key):
        if key == 8:
            try:
                self.content = self.content[0:-1]
            except:pass
        try:
            self.content += str(DateEntry.touches[key])
        except: pass
        if key == K_RETURN:
             self.subText.hide()
             if repeats['Salaire'] == 0:
                 self.subText.text = 'Veuillez renseigner un salaire'
                 self.subText.show()
             elif repeats['Description'] == 0:
                 self.subText.text = 'Veuillez renseigner une descritpion'
                 self.subText.show()
             elif repeats['Titre'] == 0:
                self.subText.text = 'Veuillez renseigner un titre'
                self.subText.show()
             elif repeats['Image'] == 0:
                 self.subText.text = 'Veuillez renseigner une image'
                 self.subText.show()
             else:
                 try:
                     if optionsSelec['Cadence'] == 'Jour par Jour':
                        addDate(self.content)
                        self.content = ''
                     elif optionsSelec['Cadence'] == 'Continue':
                        if self.title == 'Entrez une date à ajouter':
                            addDate(self.content, self.mate.content)
                        else:
                            addDate(self.mate.content, self.content)
                        self.content = ''
                        self.mate.content = ''
                            
                 except:
                     self.subText.text = 'Une erreur est survenue, veullez recommencer'
                     self.subText.show()
    def isClicked(self, b = None):
        global hitableObjects
        self.clicked = True
        self.usedColor = (0,0,255)
        hitableObjects.append(self)
    def isNotClicked(self, b = None):
        global hitableObjects
        self.clicked = False
        self.usedColor = self.baseColor
        if self in hitableObjects:
            hitableObjects.remove(self)

class TextEntry(Widget):
    touches = {K_q:"a",K_b:"b",K_c:"c",K_d:"d",K_e:"e",K_f:"f",K_g:"g",K_h:"h",K_i:"i",K_j:"j",K_k:"k",K_l:"l",K_m:"m",K_n:"n",K_o:"o",K_p:"p",K_a:"q",K_r:"r",K_s:"s",K_t:"t",K_u:"u",K_v:"v",
               K_z:"w",K_x:"x",K_y:"y",K_w:"z",K_SPACE:' ',K_0:0,K_1:1,K_2:2,K_3:3,K_4:4,K_5:5,K_6:6,K_7:7,K_8:8,K_9:9,K_KP0:0,K_KP1:1,K_KP2:2,K_KP3:3,K_KP4:4,K_KP5:5,K_KP6:6,K_KP7:7,K_KP8:8,K_KP9:9,46:'/',267:'/'}

    def __init__(self, pos, d = [450,30], content = '', size = 23, title = '', shown = True, parent = None, subText = '',launchFunc = void):
        self.title = title
        self.text = Texte(title,[pos[0], pos[1] - 20], shown = shown)
        self.launchFunc = launchFunc
        self.subText = Texte(subText, [pos[0], pos[1] + d[1] + 15], color = (255,0,0), shown = shown)
        Widget.__init__(self, pos, d, clickedFunc = self.isClicked, unclickedFunc = self.isNotClicked, listenToClicks = True, hitFunc = self.isHit, children = [self.text, self.subText], parent = parent)
        self.content = content
        self.size = size
        self.baseColor = (0,0,0)
        self.usedColor = self.baseColor
    def getTextObject(self):
        content = self.content[0:30]
        try:
            txt = pygame.font.Font(None,self.size).render(content,1,(0,0,0))
        except:
            txt = ''
            for l in content:
                try:
                    pygame.font.Font(None,self.size).render(l,1,(0,0,0))
                    txt += l
                except: pass
            txt = pygame.font.Font(None,self.size).render(txt,1,(0,0,0))
        return txt
    def draw(self):
        rect(w, self.usedColor, self.pos + self.dim, 5)
        w.blit(self.getTextObject(), [self.pos[0]+10, self.pos[1] + 8])
    def isHit(self, key):
        if key == 8:
            try:
                self.content = self.content[0:-1]
            except:pass
        elif key == K_RETURN:
            self.launchFunc(self)
        elif key == K_LCTRL:
            text = pygame.scrap.get(SCRAP_TEXT)
            if text:
                self.content = text.decode()
        try:
            if pygame.key.get_mods() & KMOD_SHIFT or  pygame.key.get_mods() & KMOD_CAPS:
               self.content += str(TextEntry.touches[key]).upper()
            else:
                self.content += str(TextEntry.touches[key])
        except: pass
        width = self.getTextObject().get_width()
        if width > self.dim[0] - 5: self.dim[0] = width + 10 
    def isClicked(self, b = None):
        global hitableObjects
        self.clicked = True
        self.usedColor = (0,0,255)
        hitableObjects.append(self)
    def isNotClicked(self, b = None):
        global hitableObjects
        self.clicked = False
        self.usedColor = self.baseColor
        if self in hitableObjects:
            hitableObjects.remove(self)

class RepeatEntry(TextEntry):
    x = 70
    y = 400
    def __init__(self, title,content = 'ù', parent = None):
        if content == 'ù': content = repeats[title]
        TextEntry.__init__(self, [RepeatEntry.x,RepeatEntry.y], title = title, parent = parent)
        RepeatEntry.y += 70
    def isHit(self, key):
        TextEntry.isHit(self, key)
        if key == K_RETURN:
            self.hide()
        repeats[self.title] = self.content
        try: self.parent.setText(self.content)
        except: pass
        
class Texte(Widget):
    def __init__(self,text, pos,color = (0,0,0), size = 17, clickedFunc = void,unclickedFunc = void, parent = None, shown = True):
        listen = False
        if clickedFunc!= void:
             listen = True
        Widget.__init__(self, pos, [(len(text) * size)/2,size], clickedFunc = clickedFunc, unclickedFunc = unclickedFunc, listenToClicks = listen, parent = parent, shown = shown)
        self.text = text
        self.color = color
        self.size = size
        print(text)
        self.transform = pygame.font.Font(None,size).render(text,1,color)
    def draw(self):
        writeW(self.text, self.pos, size = self.size, color = self.color)


class Button(Widget):
    def __init__(self,pos, text, func, d = [150, 50], c = (180,180,180), tc = (0,0,0), label = str(randrange(5000)), unclickedFunc = void, parent = None, children = [], shown = True):
          self.text = Texte(text, [pos[0] + int(d[0] / 5), pos[1] + int(d[1] /3)], size = int(sqrt((d[0]/(len(text)+1)))*6), color = tc, shown = shown)
          self.dim = d
          self.color = c
          self.textColor = tc
          self.label = label
          Widget.__init__(self,pos, d, clickedFunc = func, listenToClicks = True, unclickedFunc = unclickedFunc, parent = parent, children = children, shown = shown)
    def draw(self):
        rect(w, self.color, self.pos + self.dim)
    def show(self):
        self.text.hide()
        Widget.show(self)
        self.text.show()
    def hide(self):
        Widget.hide(self)
        self.text.hide()

class addCh(Widget):
    def __init__(self):
        self.bar = TextEntry([510,200],d = [380,30], title = 'Recherchez une ville', shown = False, launchFunc = self.searchOnline) 
        self.answerTitle = ''
        self.blocDictionnary = {}
        Widget.__init__(self, [500,100], [400,500], unclickedFunc = self.hide, children = [self.bar], shown = False)
    def chooseCh(self, text):
        menuLieu = ['Nom','Adresse','Ville','Code Postal','Pays','Site Web']
        ch = self.blocDictionnary[text.text]
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
        nouveauCh = 'Ch ' + ville
        lieu = [nouveauCh,adress,ville,code,'France',website]
        txtLieu = tabToCsv([menuLieu,lieu])
        write(txtLieu,'lieu'+ville+'.csv','utf-8')
        append('\n'+nouveauCh+',,','chs.txt','ANSI')
        print('Le Fichiers lieu ' +ville+' a été crée')
        optionsSelec['Ch'] = nouveauCh
        self.hide()
    def searchOnline(self, bar):
        try:
            soup = connect('https://etablissements.fhf.fr/annuaire/resultat.php?item=etablissement&cle=' + bar.content)
            self.answerTitle = str(soup.find('span',attrs={'class':'nombre_res'}).find('strong').string)
        except: self.answerTitle = 'Pas de résultats.'
        if self.answerTitle in ['Plus de 50 réponses trouvées.','Pas de résultats.']:
            bar.subText.text = self.answerTitle
            return 0
        else:
            bar.subText.text = 'Chosissez le Ch concerné'
            y = 260
            for bloc in soup.findAll('div',attrs={'class':'bloc_groupement'}):
                txt = bloc.find('h2').string.lstrip()
                self.children.append(Texte(txt,[510, y], clickedFunc = self.chooseCh))
                self.blocDictionnary[txt] = bloc
                y+= 20

    def draw(self):
        rect(w, (0,0,0), self.pos + self.dim, 5)
        rect(w, (255,255,255), self.pos + self.dim)
    def show(self):
        clearW()
        Widget.show(self)
        
    def hide(self):
        Widget.hide(self)
        setNewEventMenu()

class OptButton(Button):
    def __init__(self, opt, pos):
        self.title = opt[0]
        txt = opt[1]
        self.setText(txt)
        Button.__init__(self, pos, self.txt, self.clickedFunc, label = self.title, children = [Texte(self.title, [pos[0], pos[1] - 10], color = (0,0,255))],unclickedFunc = self.unclickedFunc)
        opts = optionsPos[self.title]
        self.dropDown = DropDownList([self.pos[0], self.pos[1] + 45],opts, parent = self)         
    def setText(self,txt):
        if txt == 'Modifier':
            txt = repeats[self.title]
            if txt == 0:
                txt = 'Non défini'
            if len(txt) > 10:
                txt = txt[0:10] + '...'
        self.txt = txt
        try:
            self.text.text = self.txt
        except: pass
    def clickedFunc(self, b = None):
        self.clicked = True
        self.dropDown.show()
    def unclickedFunc(self, b = None):
        self.clicked = False
    def callBack(self, txt):
        optionsSelec[self.title] = txt
        self.setText(txt)
        if optionsSelec[self.title] == 'Modifier':
            repeatEntries[self.title].setParent(self)
            repeatEntries[self.title].show()
        elif optionsSelec[self.title] == 'Ajouter un Ch':
            xx = addCh()
            xx.show()
        elif optionsSelec[self.title] == 'Continue':
            setNewEventMenu()
        elif optionsSelec[self.title] == 'Jour par Jour':
            setNewEventMenu()

class ImageDisplayer(Widget):
    def __init__(self, pos, image, dim = [175,175], color = (0,0,0), parent = None, callBack = void, shown = False, link = '', title = ''):
        Widget.__init__(self, pos, dim, listenToClicks = True, clickedFunc = self.clickedFunc, unclickedFunc = self.unclickedFunc, parent = parent, shown = shown)
        self.baseColor = color
        self.usedColor = color
        self.callBack = callBack
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, dim)
        self.link = link
        self.title = title
        if len(self.title) > 15: self.title = self.title[0:15]+'...'
        self.title = Texte(self.title, [self.pos[0]+5, self.pos[1]+5], color = (200,15,15), parent = self, shown = False)
    def clickedFunc(self, b = None):
        if not self.clicked:
            self.clicked = True
            self.usedColor = (255,0,0)
        else:
            self.callBack(self)
    def unclickedFunc(self, b =None):
        self.usedColor = self.baseColor
        self.clicked = False

    def draw(self):
        w.blit(self.image,self.pos)
        self.title.draw()
        rect(w, self.usedColor, self.pos + self.dim, 5)
        
class ImageSearcher(Widget):
    def __init__(self, b = None):
        self.cancel = Button([800,500],'Annuler',self.hide)
        self.bar = TextEntry([510,200],d = [380,30], title = "Entrez l'url vers votre image", shown = True, launchFunc = self.showImage) 
        self.blocDictionnary = {}
        Widget.__init__(self, [500,100], [400,500], unclickedFunc = self.hide, children = [self.bar, self.cancel], shown = True)
        
    def draw(self):
        rect(w, (0,0,0), self.pos + self.dim, 5)
        rect(w, (255,255,255), self.pos + self.dim)

    def show(self):
        clearW()
        Widget.show(self)
        

    def hide(self, b = None):
        Widget.hide(self)
        setNewEventMenu()

    def validate(self, b = None):
        self.hide()
        uploadImageFromUrl(self.content, optionsSelec['Ch'])
        

    def showImage(self, entry):
        try:
            i = urlopen(entry.content).read()
            imageFile = io.BytesIO(i)
            img = pygame.image.load(imageFile).convert()
        except:
            entry.subText.text = 'Url non-valide'
            return 0 
        self.children.append(ImageDisplayer([510, 250], img))
        self.children.append(Button([600,500],'Valider', self.validate))

class ImageChooser(Widget):
    def __init__(self, shown = False):
        children = [Button([100,600],'Précédent', self.previous, shown = shown), Button([1150,600], 'Suivant',self.next, shown = shown),Button([500,600],'Ajouter une image',ImageSearcher, shown = shown)]
        Widget.__init__(self, [100,50], [1200,600], shown = shown, children = children)
        self.iperpage = 15
        self.loaded = 0
        self.pages = []
        self.shownPageId = 0
        self.loadPage()

    def previous(self, b = None):
        if self.shownPageId > 0:
            for i in self.pages[self.shownPageId]:
                i.hide()
            self.shownPageId -= 1
            for i in self.pages[self.shownPageId]:
                i.show()
    def next(self, b =None):
        try:
            self.pages[self.shownPageId +1]
            for i in self.pages[self.shownPageId]:
                i.hide()
            self.shownPageId += 1
            for i in self.pages[self.shownPageId]:
                i.show()
            
        except: 
            r = self.loadPage()
            if not r: return 0
            for i in self.pages[self.shownPageId]:
                i.hide()
            self.shownPageId += 1
            for i in self.pages[self.shownPageId]:
                i.show()
        
    def callBack(self, image):
        repeats['Image'] = image.link
        self.hide()
    def loadPage(self):
        newPage = []
        x = 175
        y = 70
        try:
            images = getImages([self.loaded, self.loaded + self.iperpage])
        except: return 0
        for image in images:
            newPage.append(ImageDisplayer([x,y], image.file, parent = self, callBack = self.callBack, link = image.link, title = image.title))
            x += 200
            if x + 175 > self.pos[0] + self.dim[0]:
                x = 175
                y += 200
        self.pages.append(newPage)
        self.loaded += self.iperpage
        return 1
    
    def show(self):
        clearW()
        Widget.show(self)
        for i in self.pages[self.shownPageId]:
            i.show()
    def hide(self):
        Widget.hide(self)
        for i in self.pages[self.shownPageId]:
            i.hide()
        setNewEventMenu()
        
    def draw(self):
        rect(w, (0,0,0), self.pos + self.dim, 5)
        rect(w, (255,255,255), self.pos + self.dim)
    
def checkClicks(events):
    global w, clickableObjects
    for e in events:
        if e.type == MOUSEBUTTONUP:
            for b in clickableObjects:
                 if b in shownObjects and b.pos[0] < e.pos[0] < b.pos[0] + b.dim[0] and b.pos[1] < e.pos[1] < b.pos[1] + b.dim[1]:
                    b.clickedFunc(b)
                 else:
                    b.unclickedFunc(b)
                

def checkHits(events):
    global w, hitableObjects
    for e in events:
        if e.type == KEYDOWN:
             for o in hitableObjects:
                 o.hitFunc(e.key)

def checkEvents():
    events = pygame.event.get()
    checkClicks(events)
    checkHits(events)
def showAll():
    global w, shownObjects
    w.fill((255,255,255))
    for o in shownObjects:
        o.draw()
    flip()

def endFunc(b = None):
    global continuer
    continuer = 0
    print('YOYOY')
    saveData()
    pygame.display.quit()

def setOptionButtons():
    x = 50
    y = 25
    for k in optionsSelec.keys():
        OptButton([k, optionsSelec[k]], [x,y])
        x += 170
        if x > 1400 -170:
            x = 50
            y += 130

def setNewEventMenu(b = None):
    global w, shownObjects, clickableObjects, hitableObjects
    clearW()
    setOptionButtons()
    Button([1200, 600], 'Terminer',endFunc)
    if optionsSelec['Cadence'] == 'Jour par Jour':
        DateEntry([70,270])
    elif optionsSelec['Cadence'] == 'Continue':
        x = DateEntry([70,270])
        y = DateEntry([70,320], title = 'Entrez une date de Fin', mate = x)
        x.mate = y
    
    

def imageChooser():
    global w, shownObjects, clickableObjects, hitableObjects
    
def setInitialButtons():
    global w, shownObjects
    clearW() 
    shownButtons = [Button([550,325],'Ajouter un Evènement', setNewEventMenu),
                     Button([720,325],'Supprimer un Evènement',void)]
     
def clearW(c = (255,255,255)):
    global w, shownObjects, clickableObjects, hitableObjects
    w.fill(c)
    shownObjects = []
    clickAbleObjects = []
    hitableObjects = []

def cleanListeners():
    global w, shownObjects, clickableObjects, hitableObjects
    for o in clickableObjects:
        if o not in shownObjects:
            clickableObjects.remove(o)
    for o in hitableObjects:
        if o not in shownObjects:
            hitableObjects.remove(o)

repeatEntries = {'Titre':RepeatEntry('Titre'),'Description':RepeatEntry('Description'),'Salaire':RepeatEntry('Salaire'), 'Image':ImageChooser()}
data = getChs()
for ch in data:
    optionsPos["Ch"].append(ch)
optionsPos["Ch"].append('Ajouter un Ch')
