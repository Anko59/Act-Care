def garde(date):
    jour = int(date[0:2])
    
cH = input('Nom du centre Hospitalier')
spe = input('Specialité recherchée')
titre = input('Titre de la mission')
image = input("Nom de l'image mise en avant")
infoT = input("Informations transport")
nbrDates = input('Combien de Dates allez vous rentrer ?')
formatHoraires = {'Garde':'8h00/8h00','Journée':'08h30/18h30','Nuit':'20h00/8h00'}
mois = {'01':'Janvier','02':'Février','03':'Mars','04':'Avril','05':'Mai','06':'Juin','07':'Juillet','08':'Aout','09':'Septembre','10':'Octobre','11':'Novembre','12':'Décembre'}
monthes = {'01':'Jan','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun','07':'Juil','08':'Aug','09':'Sept','10':'Oct','11':'Nov','12':'Dec'}
dates = []
horaires = []
print('Format dates: J/M/Y')
print("Format Horaires: Garde, Journée, Nuit, ou XXhXX/XXhXX")
for date in range(int(nbrDates)):
    dates.append(input('Date '+str(date)+':'))
    horaire = input('Horaire de début '+str(date)+':')
    try: horaire = formatHoraires[horaire]
    except: pass
    horaires.append(horaire)
events = []
'EVENT NAME,VENUE NAME,ORGANIZER NAME,START DATE,START TIME,END DATE,END TIME,ALL DAY EVENT?,CATEGORIES,EVENT COST,EVENT PHONE,EVENT WEBSITE,SHOW MAP LINK?,SHOW MAP?,EVENT DESCRIPTION'
for i in range(len(dates)):
    """daTe = dates[i].split('/')
    date = daTe[2]+daTe[1]+daTe[0]
    horaire = horaires[i].split('/')
    start = horaire[0].replace('h','')+'00'
    end = horaire[1].replace('h','')+'00'
    startDate = date+'T'+start
    endDate = date+'T'+end"""
    date = dates[i].split('/')
    startDate = monthes[date[1]]+ " " + date[0]+", "+date[2]
    
    info = 'Le '+cH+' recherche un remplaçant en '+spe+" le " + daTe[0] + mois[daTe[1]]" de " + horaires[i]
    infos = info +'\n'+infoT
    
with open('Event '+cH+' '+ str(i)+'.ics','w') as file:
    file.write(txt)
    
