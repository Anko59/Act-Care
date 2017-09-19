Chs = []
nomsChs = []
contacts = []
codesChs = {}
with open('chCodes.csv','r') as file:
    txt = file.read()
    lines = txt.split("\n")
    for line in lines:
        line = line.split(',')
        name = str(line[3])
        codesChs[name] = [line[0],line[1],line[2]]
    file.close()
class Contact:
    def __init__(self, nom, service,phone, mail, ch,prio_contact, ville, region, code_postal):
        self.nom = nom
        self.phone = phone
        self.mail = mail
        self.service = service
        self.ch = ch
        self.prio = prio_contact
        self.ville = ville
        self.region = region
        self.code_postal = code_postal
        contacts.append(self)
        print(self.mail)
    def output(self):
        txt = ""
        for data in [self.nom, self.ch,self.service, self.phone, self.mail,self.prio,self.ville,self.region,self.code_postal]:
            txt += data + ","
        return (txt + "\n")
class Ch:
    def __init__(self,statut, info_relance,region,code_postal,ville, nom,spe, prio_contact, nom_contact, service, phone, mail,t,date1ercontact, info1ercontact, date2emecontact, info2emecontact,datexcontact,infoxcontact):
        if statut == "": self.statut = "a prospecter"
        else: self.statut = statut
        self.info_relance = info_relance
        self.code_postal = code_postal
        self.nom = nom
        self.infoContacts = ""
        if date1ercontact != "" or info1ercontact != "":
            self.infoContacts += date1ercontact +": "+info1ercontact
        if date2emecontact !="" or info2emecontact != "":
            self.infoContacts += " --- "+date2emecontact + ": "+info2emecontact
        if datexcontact != "" or infoxcontact != "":
            self.infoContacts += " --- " + datexcontact + ": " +infoxcontact
        if 'prospecter' in self.statut:
            if self.infoContacts != "":
                self.statut = "prospecte"
            else: self.statut = "a prospecter"
        self.dateDernierContact = ""
        for date in [date1ercontact, date2emecontact,datexcontact]:
            if date != "": self.dateDernierContact = date
        self.code_postal = code_postal
        self.region = region
        self.ville = ville
        if nom_contact != "" or service != "" or phone != "" or mail != "":
            cnt = Contact(nom_contact, service, phone, mail, nom,prio_contact,self.ville, self.region, self.code_postal)
        if self.nom not in nomsChs:
            Chs.append(self)
            nomsChs.append(self.nom)
    def output(self):
        txt = ""
        for data in [self.statut, self.info_relance,self.region, self.code_postal, self.ville, self.nom,self.infoContacts,self.dateDernierContact]:
            txt += data+","
        return (txt + "\n")

def treatData():
    with open("pythonCh.csv", "r") as fichier:
        fullText = fichier.read()
        fullText = fullText.split("\n")
        for line in fullText:
            line = line.split(",")
            ch = Ch(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18])
        fichier.close()

def outputChs():
    with open("chsDefinitifs.csv","w") as file:
        txt = ""
        for ch in Chs:
            txt += ch.output()
        file.write(txt)
        file.close()

def outputContacts():
    with open ("contact.csv","w") as file:
        txt = ""
        for contact in contacts:
            txt += contact.output()
        file.write(txt)
        file.close()

if __name__ == '__main__':
    treatData()
    outputChs()
    outputContacts()
