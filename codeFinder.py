chs = []
with open('hopitaux.csv','rb') as file:
    txtHopitaux = file.read().decode()
    listHopitaux = txtHopitaux.split('\n')
    file.close()

codes = {}
with open('codes.csv','rb') as file:
    txtCodes = file.read().decode()
    listCodes = txtCodes.split('\n')
    file.close()

regions = {}
with open('departement.csv','rb') as file:
    txtRegions = file.read().decode()
    listRegions = txtRegions.split('\n')
    file.close()

class Ch:
    def __init__(self, code, ville, nom, prio, interloc, service, phone, mail):
        self.ville = ville
        self.nom = nom
        self.prio = prio
        self.interloc = interloc
        self.service = service
        self.phone = phone
        self.mail = mail
        if code == "":
            ville = ville.replace("ç","c")
            ville = ville.replace("é","e")
            ville = ville.replace("è","e")
            ville = ville.replace('Saint','St')
            ville = ville.replace('-',' ')
            ville = ville.replace("'",' ')
            ville = ville.replace("à","a")
            ville = ville.replace('â',"a")
            try:
                self.code = codes[ville.upper()]
            except:
                self.code = ""
        else:
            self.code = code
        try:
            self.region = regions[self.code[0:2]]
        except:self.region = ""
        chs.append(self)
    def output(self):
        txt = ""
        for x in [self.code, self.ville, self.nom, self.prio, self.interloc, self.service, self.phone, self.mail]:
            txt += (x + ",")
        self.code = self.code.replace('\n','')
        return (self.region.capitalize() + "\n")

def treatData():
    for line in listCodes:
        data = line.split(',')
        codes[data[0]] = data[1]
    for line in listRegions:
        data = line.split(',')
        regions[data[1]] = data[2].upper()
    for line in listHopitaux:
        data = line.split(',')
        Ch(data[0], data[1],data[2],data[3],data[4],data[5],data[6],data[7])

def outputData():
    with open("NewHopitaux.csv", "wb") as file:
        txt = ""
        for ch in chs:
            txt += ch.output()
        print(txt)
        file.write(txt.encode())
        file.close()

if __name__ == '__main__':
    treatData()
    outputData()
