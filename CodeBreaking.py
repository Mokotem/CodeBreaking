# -*- coding: latin-1 -*-

tailleFenetre = (720, 720)  # taille de la fenètre



# --- PARTIE 1 : FONCTIONS ---


# - FONCTIONS DE DESSIN -
def factoriel(njeton, ncolonne):
    n = 1
    for i in range(ncolonne):
        n *= (njeton - i)
    return n

def ecranVersPan(posi):  # transforme une coordonné de l'écran vers un plan (origine au centre et ordonnés vers le haut)
    return (posi[0] - (tailleFenetre[0]/2), (-posi[1]) + (tailleFenetre[1]/2))

def planVersEcran(posi):  # réciproque de 'ecranVersPan'
    return (posi[0] + (tailleFenetre[0]/2), -(posi[1] - (tailleFenetre[1]/2)))

def dessinerTexte (text, posi, taille, color, centerX):
    font = game.font.Font(police, taille)
    text = font.render(text, True, color)
    textOffset = text.get_rect()

    textPos = planVersEcran(posi)

    if (centerX == False):
        textOffset = (0, 0, textOffset[0], textOffset[3])

    background.blit(text, (textPos[0] - (textOffset[2]/2), textPos[1] - (textOffset[3]/2)))

def dessinerImage(sprite, posi, taille):  # déssine une image
               newSprite = game.transform.smoothscale(sprite, taille)
               posi = list(posi)
               posi[1] = -posi[1]
               posi = planVersEcran(posi)
               spriteX = newSprite.get_size()[0]
               spriteY = newSprite.get_size()[1]
               posX = posi[0] - (spriteX//2)
               posY = posi[1] - (spriteY//2)

               background.blit(newSprite, (posX, posY))
               return sprite

def dessinerRectange(posi, taille, couleur):
    bouton = _bouton()
    bouton.position = planVersEcran(posi)
    bouton.taille = taille
    rectangle = game.Rect(bouton.position[0] - (bouton.taille[0]/2), bouton.position[1] - (bouton.taille[1]/2), bouton.taille[0], bouton.taille[1])
    game.draw.rect(background, couleur, rectangle)

def createBouton (text, posi, taille, centerX, active):  # crée un bouton
        font = game.font.Font(police, 20)

        bouton = _bouton()
        bouton.position = planVersEcran(posi)
        bouton.taille = taille
        rectangle = game.Rect(bouton.position[0] - (bouton.taille[0]/2), bouton.position[1] - (bouton.taille[1]/2), bouton.taille[0], bouton.taille[1])
        bouton.position = tuple(posi)
        conditionX = bouton.position[0] + (bouton.taille[0]/2) >= souris.position[0] and souris.position[0] >= bouton.position[0] - (bouton.taille[0]/2)
        conditionY = bouton.position[1] + (bouton.taille[1]/2) >= souris.position[1] and souris.position[1] >= bouton.position[1] - (bouton.taille[1]/2)
        boutonPresse = False
        if (active):
            if (conditionX and conditionY):
                if (souris.boutonGauche):
                    boutonPresse = True
                    game.draw.rect(background, (inputColor[0]//1.5, inputColor[1]//1.5, inputColor[2]//1.5), rectangle)
                else:
                    game.draw.rect(background, (255, 222, 199), rectangle)

            else:
                game.draw.rect(background, inputColor, rectangle)
        else:
            game.draw.rect(background, (inputColor[0]//1.5, inputColor[1]//1.5, inputColor[2]//1.5), rectangle)

        dessinerTexte (text, (posi[0], posi[1] - 2), 25, (0, 0, 0), True)

        return boutonPresse

def createJeton (posi, taille, sprite, active, suppr):  # crée un jeton (variante de bouton)
        bouton = _bouton()
        if (not suppr):
            bouton.chiffre = spritesJeton.index(sprite)
        bouton.position = planVersEcran(posi)
        bouton.taille = taille
        rectangle = game.Rect(bouton.position[0] - (bouton.taille[0]/2), bouton.position[1] - (bouton.taille[1]/2), bouton.taille[0], bouton.taille[1])
        bouton.position = ecranVersPan(bouton.position)
        monPotoPythagore = math.sqrt(((souris.position[0] - posi[0]) ** 2) + ((souris.position[1] + posi[1]) ** 2))
        bouton.presse = False

        if (active):
            if (monPotoPythagore <= 30):
                if (souris.boutonGauche):
                    bouton.presse = True
        if (keyBoard[bouton.chiffre] == True):
            bouton.presse = True

        dessinerImage(sprite, bouton.position, bouton.taille)

        return bouton

def afficherPartie (partie, parametres, reveler):  # affiche la partie
      tailleJeton = min(80, min(300 // parametres.colonne, 500 // parametres.ligne))

      tailleCodeX = min(60 * parametres.colonne, 540)
      for i in range(parametres.colonne):
            if (reveler):
                dessinerImage(spritesJeton[partie.code[i]],\
                     (int((((i+0.5) / parametres.colonne) - 0.5) * tailleCodeX), -320),\
                     (tailleCodeX // parametres.colonne, tailleCodeX // parametres.colonne))
            else:
                dessinerImage(spriteMystere,\
                     (int((((i+0.5) / parametres.colonne) - 0.5) * tailleCodeX), -320),\
                     (tailleCodeX // parametres.colonne, tailleCodeX // parametres.colonne))

      for ligne in range(parametres.ligne):
            for colonne in range(parametres.colonne):
                  dessinerImage(spritesJeton[partie.grilleJoueur[parametres.ligne - ligne - 1][colonne]], \
                  (int(((colonne / parametres.colonne) - 0.5) * 300 - 100), int(((ligne / parametres.ligne) - 0.5) * 500 + 30)),\
                  (tailleJeton, tailleJeton))
            i = 0
            for sprite in partie.correction[ligne]:
                  dessinerImage(spritesPlace[int(sprite)],\
                  (((i / parametres.colonne) - 0.5) * 100 + 100, int((((parametres.ligne - ligne - 1) / parametres.ligne) - 0.5) * 500 + 30)),\
                  (int(100 // parametres.colonne//1.2), int(100 // parametres.colonne//1.2)))
                  i += 1

def mettreCouleurJetons (sprites):
    for i in range(parametres.jeton + 1):
        if (i > 0):
            sprites[i] = copySpritesJeton[i].copy()
            couleur = game.Color(0)
            c = int((i) / (parametres.jeton) * 360)
            couleur.hsla = (c, 100, 60, 100)
            sprites[i].fill(couleur, special_flags=game.BLEND_RGB_MULT)

class _curseur:  # type souris
               position = (0, 0)
               boutonGauche = False
               boutonDroit = False
               molette = 0

souris = _curseur()

import random
import math
import time


# - FONCTIONS DU JEU -

class _partie:  # type partie
    code = []
    grilleJoueur = []
    correction = []

class _parametre:  # type paramètres
    colonne = 0
    ligne = 0
    jeton = 0
    couleurUni = False
    modeNoobs = False

class _bouton:  # type bouton
    presse = False
    chiffre = 0
    position = (0, 0)
    taille = (0, 0)

def nouvellePartie(parametre): # Romain  # crée une nouvelle partie selon des parramètres
    
    # création du type 'partie' vierge.
    partie = _partie()
    partie.grilleJoueur = []
    partie.code = []
    partie.correction = []

    # remplissage de la grille de jeux avec des jetons vides, selons le nombre de colonne et lignes.
    for i in range(parametre.ligne):
        ligne = []
        correc = []
        for j in range(parametre.colonne):
            ligne.append(0)
            correc.append(existePas)

        partie.grilleJoueur.append(ligne)
        partie.correction.append(correc)

    # création du code secret de la partie
    if not parametres.couleurUni:
        # mode couleurs aléatoires
        for i in range(parametre.colonne):
            partie.code.append(random.randint(1, parametre.jeton))
    else:
        # mode couleurs uniques
        jetonsRestants = []
        for i in range(parametres.jeton):
            jetonsRestants.append(i+1)
        for i in range (parametres.colonne):
            j = random.randint(0, len(jetonsRestants)-1)
            partie.code.append(jetonsRestants[j])
            jetonsRestants.pop(j)
            
    return partie

def correction (ligne, code, parametres): # Louis  # retourne la correction d'une ligne
    resultat = []
    utilisateurCopy = list(ligne)
    codeCopy = list(code)

    # correction relative à la position des jetons
    if (parametres.modeNoobs):
        utilisateurCopy = list(code)
        for i in range(parametres.colonne):
            resultat.append(existePas)
        for indexe in range(len(code)):
            if (code[indexe] == ligne[indexe]):
                utilisateurCopy.remove(code[indexe])
                resultat[indexe] = bienPlace
            elif ligne[indexe] in utilisateurCopy:
                resultat[indexe] = malPlace
            else:
                resultat[indexe] = existePas

    else:
        # correction relative à la position des jetons
        
        # on commence par les biens placé
        for indexe in range(len(code)):
            if (code[indexe] == ligne[indexe]):
                resultat.append(bienPlace)
                utilisateurCopy.remove(code[indexe])
                codeCopy.remove(code[indexe])

        # on note mal placé si il n'est pas déja trouvé
        while len(utilisateurCopy) > 0:
            if (utilisateurCopy[0] in codeCopy):
                resultat.append(malPlace)
                codeCopy.remove(utilisateurCopy[0])
            else:
                resultat.append(existePas)

            utilisateurCopy.pop(0)

            resultat.sort()

    return resultat

def possibilite (parametres): # Louis  # calcules le nombre de possibilité de code en fonction des parramètres
    # calcules de maths
    if (parametres.couleurUni):
        return factoriel(parametres.jeton, parametres.colonne)
    else:
        return parametres.jeton ** parametres.colonne

def difficulte (parametres): # Romain  # calcule la difficultée d'un parramètre de partie
    return min(round((possibilite(parametres) / parametres.ligne ** 2) * 50), 100)
    
# - AUTRES -
def sauvegarder(p): # sauvegarde les points du joeur
    with open("ressources/sauvegarde.txt", "w") as s:
        s.truncate(0)
        s.write(str(p))
    



# --- PARTIE 2 : STRUCTURE ---
# Partie 2 faite en simultané avec Romain et Louis en cours et distantiel.


import pygame as game
from pygame.locals import *

# palette de couleurs
bgColor = (22, 18, 11)
mgColor = (41, 76, 96)
textColor = (255, 239, 211)
inputColor = (255, 196, 155)
otherColor = (173, 182, 196)

taillePolice = 25

game.init()

fenetre = game.display.set_mode(tailleFenetre)
game.display.set_caption("Code Breaking")

background = game.Surface(fenetre.get_size())
background = background.convert()

# parramètres par défaut
parametres = _parametre()
parametres.colonne = 5
parametres.ligne = 9
parametres.jeton = 6

nJeton = 5


# - chargement des sprites -

spritesJeton = []
copySpritesJeton = []

n = 1

for i in range(10):
   spritesJeton.append(game.image.load("ressources/sprite"+str(n)+"/sprite"+str(i)+".png").convert())
copySpritesJeton = spritesJeton.copy()

bienPlace = "0"
malPlace = "1"
existePas = "2"
spriteMystere = game.image.load("ressources/jetonSecret.png").convert()
spriteCurseur = game.image.load("ressources/curseur.png").convert()
spriteSupprimer = game.image.load("ressources/delete.png").convert()

spritesPlace = [game.image.load("ressources/existe.png").convert(), game.image.load("ressources/malPlace.png").convert(), game.image.load("ressources/existePas.png").convert()]

# création de la partie
partie = nouvellePartie(parametres)
essaiActuel = 0
colonneActuel = 0
reponse = []

mettreCouleurJetons(spritesJeton)

police = "ressources/Celeste_Font.ttf"
game.time.Clock().tick(60)

onBoutonSouris = False
running = True
finDePartie = False

timer = 2

menu = "menu"
sauvegarde = open("ressources/sauvegarde.txt", "r")
points = int(sauvegarde.read())
pointsMis = False

while running:
    # --- INPUTS ---
    boutonEntrer = False
    boutonSuppr = False

    if (menu == "parametres" or menu == "menu" or menu == "infos"):
        background.fill(bgColor)
    else:
        background.fill((0, 0, 0))
    souris.boutonGauche = False
    keyBoard = []
    for i in range (10):
        keyBoard.append(False)

    for evenement in game.event.get():
        if (evenement.type == QUIT):
            running = False

        if evenement.type == KEYDOWN:
            if evenement.key == K_0: keyBoard[0] = True
            elif evenement.key == K_1: keyBoard[1] = True
            elif evenement.key == K_2: keyBoard[2] = True
            elif evenement.key == K_3: keyBoard[3] = True
            elif evenement.key == K_4: keyBoard[4] = True
            elif evenement.key == K_5: keyBoard[5] = True
            elif evenement.key == K_6: keyBoard[6] = True
            elif evenement.key == K_7: keyBoard[7] = True
            elif evenement.key == K_8: keyBoard[8] = True
            elif evenement.key == K_9: keyBoard[9] = True
            elif evenement.key == K_BACKSPACE: boutonSuppr = True
            elif evenement.key == K_RETURN: boutonEntrer = True


        if (onBoutonSouris and menu != "magasin"): souris.boutonGauche = False

        if (game.mouse.get_pressed()[0] == True and onBoutonSouris == False):
            souris.boutonGauche = True
            onBoutonSouris = True

        if (game.mouse.get_pressed()[0] == False):
            onBoutonSouris = False

        souris.boutonDroit = game.mouse.get_pressed()[2]
        souris.position = ecranVersPan(game.mouse.get_pos())

    # --- MAIN ---
    if (menu == "jouer"):
        afficherPartie(partie, parametres, finDePartie)

        if not finDePartie:
            dessinerImage(spriteCurseur, (-310, int((((parametres.ligne - essaiActuel - 1) / parametres.ligne) - 0.5) * 500 + 30)), (20, 20))

        #  boutons pour choisir les couleurs
        boutons = []
        taille = 62 * (parametres.jeton + 1)
        for i in range(parametres.jeton):
            boutons.append(createJeton((((i/(parametres.jeton)) - 0.5) * taille, 310), (60, 60), spritesJeton[i+1], True, False))
        boutonSupprimer = createJeton(((0.5 * taille), 310), (60, 60), spriteSupprimer, True, True)

        #  quand la partie est finito
        if finDePartie:
            dessinerTexte("[entrer]", (250, -100), 30, (200, 200, 200), True)
            if boutonEntrer:
                partie = nouvellePartie(parametres)
                essaiActuel = 0
                colonneActuel = 0
                reponse = []
                finDePartie = False


        if (not finDePartie):
            pointsMis = False
            for bouton in boutons:
                if (bouton.presse):
                    partie.grilleJoueur[essaiActuel][colonneActuel] = bouton.chiffre
                    colonneActuel += 1

                    if (colonneActuel > parametres.colonne - 1):
                        partie.correction[essaiActuel] = correction(partie.grilleJoueur[essaiActuel], partie.code, parametres)

                        essaiActuel += 1
                        colonneActuel = 0

                    break

            if createBouton(">", (250, 0), (60, 60), True, True):
                menu = "menu"
            dessinerTexte("Menu", (250, 50), 30, textColor, True)

            finDePartie = essaiActuel > parametres.ligne -1 or partie.grilleJoueur[essaiActuel - 1] == partie.code
        else:
            if (partie.grilleJoueur[essaiActuel - 1] == partie.code):
                dessinerTexte("gagnée !", (250, 200), 40, textColor, True)
                if parametres.modeNoobs == False:
                    paraLigne = int(parametres.ligne)
                    parametres.ligne = int(essaiActuel)
                    dessinerTexte("points +"+str(difficulte(parametres)), (250, 100), 30, textColor, True)
                    if not pointsMis:
                        points += difficulte(parametres)
                        pointsMis = True
                    
                    sauvegarder(points)
                    parametres.ligne = int(paraLigne)
            else:
                dessinerTexte("perdu.", (250, 200), 40, textColor, True)
            dessinerTexte("en "+str(essaiActuel)+" essais", (250, 150), 25, textColor, True)

        if ((boutonSupprimer.presse or boutonSuppr) and colonneActuel > 0):
            partie.grilleJoueur[essaiActuel][colonneActuel - 1] = 0
            colonneActuel -= 1

    elif menu == "parametres":
        dessinerTexte("OPTIONS", (0, 300), round(taillePolice * 1.5), textColor, True)

        dessinerTexte("Colonnes : ", (-250, 150), taillePolice, textColor, False)
        if createBouton("-", (-50, 150), (40, 40), True, parametres.colonne > 2):
             parametres.colonne -= 1
        dessinerTexte(str(parametres.colonne), (0, 150), taillePolice, textColor, True)
        if createBouton("+", (50, 150), (40, 40), True, parametres.colonne < 20 and not (parametres.couleurUni and (parametres.colonne >= parametres.jeton))):
             parametres.colonne += 1
        dessinerTexte("min:2    max:20", (100, 150), taillePolice, textColor, False)

        dessinerTexte("Lignes : ", (-250, 100), taillePolice, textColor, False)
        if createBouton("-", (-50, 100), (40, 40), True, parametres.ligne > 2):
             parametres.ligne -= 1
        dessinerTexte(str(parametres.ligne), (0, 100), taillePolice, textColor, True)
        if createBouton("+", (50, 100), (40, 40), True, parametres.ligne < 40):
             parametres.ligne += 1
        dessinerTexte("min:2    max:40", (100, 100), taillePolice, textColor, False)

        dessinerTexte("Jetons : ", (-250, 50), 30, textColor, False)
        if createBouton("-", (-50, 50), (40, 40), True, parametres.jeton > 2):
             parametres.jeton -= 1
        dessinerTexte(str(parametres.jeton), (0, 50), taillePolice, textColor, True)
        if createBouton("+", (50, 50), (40, 40), True, parametres.jeton < 9):
             parametres.jeton += 1
        dessinerTexte("min:2    max:9", (100, 50), taillePolice, textColor, False)

        dessinerTexte("Couleurs uniques : ", (-250, -50), taillePolice, textColor, False)
        if createBouton("oui", (50, -50), (80, 30), True, not parametres.couleurUni): parametres.couleurUni = True
        if createBouton("non", (150, -50), (80, 30), True, parametres.couleurUni): parametres.couleurUni = False
        dessinerTexte("les couleurs ne peuvent pas se répéter dans le code.", (-250, -71), taillePolice//2, textColor, False)

        dessinerTexte("Mode apprenti : ", (-250, -100), taillePolice, textColor, False)
        if createBouton("oui", (50, -100), (80, 30), True, not parametres.modeNoobs): parametres.modeNoobs = True
        if createBouton("non", (150, -100), (80, 30), True, parametres.modeNoobs): parametres.modeNoobs = False
        dessinerTexte("les resultats sont relatif a la position.", (-250, -121), taillePolice//2, textColor, False)

        if (parametres.couleurUni and (parametres.colonne > parametres.jeton)):
            parametres.colonne = parametres.jeton

        nPossibilite = possibilite(parametres)

        if len(str(nPossibilite)) < 11:
            dessinerTexte("Nombre de possiblité :  "+str(nPossibilite), (-250, -150), 30, textColor, False)
        else:
            dessinerTexte("Nombre de possiblité :  9999999999+", (-250, -150), 30, textColor, False)
        dessinerTexte("Combinaisons possibles de codes.", (-250, -171), taillePolice//2, textColor, False)

        if (parametres.modeNoobs):
            dessinerTexte("Difficultée :  apprenti / 100", (-250, -200), taillePolice, textColor, False)
        else:
            dessinerTexte("Difficultée :  "+str(difficulte(parametres))+" / 100", (-250, -200), taillePolice, textColor, False)
        dessinerTexte("équivalent aux points gagnés. (le gain est ajusté si le code est trouvé plus rappidement)", (-250, -220), taillePolice//2, textColor, False)

        if (createBouton("options par défaut", (-110, 220), (280, 30), True, True)):
            parametres = _parametre()
            parametres.colonne = 5
            parametres.ligne = 9
            parametres.jeton = 6

        if (createBouton("ok", (0, -310), (120, 40), True, True)):
             menu = "menu"
             partie = nouvellePartie(parametres)
             essaiActuel = 0
             colonneActuel = 0
             reponse = []
             finDePartie = False
             spritesJeton = list(copySpritesJeton)
             mettreCouleurJetons(spritesJeton)
             
    elif menu == "menu":
        dessinerTexte("CODE BREAKING", (0, 200), 30, textColor, True)
        dessinerTexte(str(points)+" points", (0, 170), 25, textColor, True)
        
        if createBouton("options", (0, 0), (150, 60), True, True):
            menu = "parametres"
        if createBouton("infos", (0, 75), (150, 60), True, True):
            menu = "infos"
        if createBouton("quiter", (0, -75), (150, 60), True, True):
            running = False
        if createBouton("sauvegarder", (200, -75), (200, 60), True, True):
            sauvegarder(points)
            timer = time.monotonic()
            menu = "save"
            
        if createBouton("récompenses", (200, 0), (200, 60), True, True):
            menu = "magasin"
            

        if createBouton("<", (-250, 0), (60, 60), True, True):
                menu = "jouer"
        dessinerTexte("Jouer", (-250, 50), 30, textColor, True)

    elif (menu == "infos"):
        dessinerTexte("INFOS", (0, 280), 40, textColor, True)

        dessinerTexte("Utilisez les boutons pour ajouter", (-200, 200), 20, textColor, False)
        dessinerTexte("ou supprimer un jeton", (-200, 200 - 20), 20, textColor, False)

        dessinerImage(spritesJeton[1], (-280, -200 + 20 + 50), (60, 60))

        dessinerTexte("Utilisez le clavier pour placer", (-200, 200 - 20 - 40), 20, textColor, False)
        dessinerTexte("des chiffres rapidement.", (-200, 200 - 80), 20, textColor, False)

        dessinerTexte("Touches [0] ou [<--] pour supprimer", (-200, 200 - 80 - 40), 20, textColor, False)
        dessinerTexte("le dernier jeton.", (-200, 200 - 80 - 60), 20, textColor, False)

        dessinerTexte("Personalisez votre jeu dans les", (-200, 200 - 80 - 100), 20, textColor, False)
        dessinerTexte("options.", (-200, 200 - 80 - 120), 20, textColor, False)

        dessinerImage(spritesPlace[0], (-280, -200 + 80 + 160), (35, 35))
        dessinerTexte("Bien placé", (-200, 200 - 80 - 160), 20, textColor, False)

        dessinerImage(spritesPlace[1], (-280, 80), (35, 35))
        dessinerTexte("Mal placé", (-200, -80), 20, textColor, False)
        
        dessinerTexte("Récupérez vos récompenses au", (-200, -140), 20, textColor, False)
        dessinerTexte("menu principale.", (-200, -160), 20, textColor, False)

        if (createBouton("ok", (0, -310), (120, 40), True, True)):
            menu = "menu"
    elif menu == "save":
        background.fill(bgColor)
        dessinerTexte("sauvegardé !", (0, 0), 30, textColor, True)
        if (time.monotonic() - timer > 1):
            menu = "menu"
    elif menu == "magasin":
        dessinerTexte(str(points)+" points", (0, 320), 35, textColor, True)
        boutons = []
        for i in [1, 2, 3, 4, 5]:
            dessinerTexte("Jetons n°"+str(i), (-300, (i-1) * 90 - 120), 20, textColor, False)
            if i == 5 and points < 400:
                dessinerTexte("Débloquez ces jetons pour les révéler.", (-300, (i-1) * 90 - 150), 15, textColor, False)
            else:
                for j in range (9):
                    p = game.image.load("ressources/sprite"+str(i)+"/sprite"+str(j)+".png").convert()
                    dessinerImage(p, (j*30 - 280, ((-i+5) * 90) - 280 + 75), (30, 30))
            if (i > 1):
                dessinerTexte(str(50 * (2**(i - 2)))+" points", (0, (i-1) * 90 - 120), 20, textColor, True)
                cond = points >= 50 * (2**(i - 2))
            else:
                cond = True
            boutons.append(createBouton("choisir", (250, (i-1) * 90 - 120), (150, 40), True, cond))
        for i in range(1, nJeton+1):
            if boutons[i - 1]:
                n = int(i)
                spritesJeton = []
                copySpritesJeton = []
                for j in range(10):
                    spritesJeton.append(game.image.load("ressources/sprite"+str(n)+"/sprite"+str(j)+".png").convert())
                copySpritesJeton = spritesJeton.copy()
                mettreCouleurJetons(spritesJeton)
        
        dessinerImage(spritesJeton[0], (0, 230), (80, 80))
        if (createBouton("ok", (0, -310), (120, 40), True, True)):
            menu = "menu"



    fenetre.blit(background, (0, 0))
    game.display.flip()

game.quit()