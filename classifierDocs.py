doctors = {}
regions = {}
with open('departement.csv','rb') as file:
    txtRegions = file.read().decode()
    listRegions = txtRegions.split('\n')
    file.close()
class Doctor:
    def __init__(self, inscr,nom, prenom, ddn, spe,mail, phone1,phone2,address,code,ville,ouvert,reponse, rempla, smur, freq,media,pref,camu,dossier):
        self.inscr = inscr
        self.nom = nom
        self.prenom = prenom
        self.ddn = ddn
        self.spes = spe
        self.mail = mail
        self.phone1 = phone1
        self.phone2 = phone2
        self.address = address
        self.code = code
        self.ville = ville
        self.ouvert = ouvert
        self.reponse = reponse
        self.rempla = rempla
        self.smur = smur
        self.freq = freq
        self.media = media
        self.pref = pref
        self.camu = camu
        self.dossier = dossier
        try:
            self.region = regions[self.code[0:2]]
            
        except:
            self.region = ""
        self.content = [self.inscr,self.nom,self.prenom, self.ddn,self.spes,self.mail.lower(), self.phone1, self.phone2, self.address, self.code,self.ville, self.region,self.ouvert,self.reponse,self.rempla,self.smur,self.freq,self.media,self.pref,self.camu,self.dossier]
        if self.fullName() in doctors.keys():
            if spe not in doctors[self.fullName()].spes:
                doctors[self.fullName()].spes += (" - "  + spe)
            for i in range(len(doctors[self.fullName()].content)):
                if doctors[self.fullName()].content[i] == "" and self.content[i] != "":
                    doctors[self.fullName()].content[i] = self.content[i]
        else:
            doctors[self.fullName()] = self
    def fullName(self):
        return self.prenom +" "+ self.nom
    def output(self):
        txt = ""
        for x in self.content:
            txt += x+","
        return (txt +'\n')

def treatData():
    for line in listRegions:
        data = line.split(',')
        regions[data[1]] = data[2].upper()
    with open('allDoctors1.csv','rb') as file:
        text = file.read().decode()
        text = text.split('\n')
        for line in text:
            data = line.split(',')
            for x in range(len(data)):
                data[x] = data[x].capitalize()
            Doctor(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18],data[19])
        file.close()

def outputData():
    with open('allDoctors3.csv',"w") as file:
        txt = ""
        for key in doctors.keys():
            doc = doctors[key]
            txt += doc.output()
        file.write(txt)
        file.close()

if __name__ == '__main__':
    treatData()
    outputData()
