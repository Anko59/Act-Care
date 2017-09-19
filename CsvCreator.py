from graphics2 import *
"""ch = findCh().replace('\r','')
displaySelectedOptions()
print("Entrez 'options' ou 'o' pour modifier les options")
print("Entrez 'fin' pour terminer.")
print("Entrez 'cancel' pour annuler une date")"""
setInitialButtons()
global continuer
while continuer:
    showAll()
    checkEvents()
    
saveData(ch)
pygame.display.quit()
