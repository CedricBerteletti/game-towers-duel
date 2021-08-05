#!/usr/bin/python
# coding: utf-8

import pygame
import math
#from pygame.locals import *
from joueurs import Joueur
from decors import Desert
from vecteurs import Vecteur

# Constantes
LARGEUR_ECRAN = 900
HAUTEUR_ECRAN = 600
DELTA_FORCE = 3
DELTA_ANGLE = math.pi / 40


# DEBUG
def dessiner_croix(surface, x, y):
    pygame.draw.line(surface, (0, 0, 0), (x-1, y), (x+1, y))
    pygame.draw.line(surface, (0, 0, 0), (x, y-1), (x, y+1))


def init_joueur(numero, nom, x, y, vitesse, couleur):
    joueur = Joueur(numero, nom, x, y)
    joueur.tir.vecteur = vitesse
    joueur.tir.couleur = couleur
    return joueur


def gerer_action(event, joueur1, joueur2, projectiles, projectiles_de_ciment):
    if event.key == pygame.K_z:
        joueur1.changer_angle(-DELTA_ANGLE)
    elif event.key == pygame.K_s:
        joueur1.changer_angle(DELTA_ANGLE)
    elif event.key == pygame.K_q:
        joueur1.changer_force(-DELTA_FORCE)
    elif event.key == pygame.K_d:
        joueur1.changer_force(DELTA_FORCE)
    elif event.key == pygame.K_DOWN:
        joueur2.changer_angle(-DELTA_ANGLE)
    elif event.key == pygame.K_UP:
        joueur2.changer_angle(DELTA_ANGLE)
    elif event.key == pygame.K_RIGHT:
        joueur2.changer_force(-DELTA_FORCE)
    elif event.key == pygame.K_LEFT:
        joueur2.changer_force(DELTA_FORCE)
    elif event.key == pygame.K_SPACE:
        if joueur1.rechargement >= 50:
            # if joueur1.compteur_de_tirs == 5:
            #     joueur1.rechargement = joueur1.rechargement - 50
            #     joueur1.compteur_de_tirs = joueur1.compteur_de_tirs - 5
            #     p = joueur1.tirer_ciment()
            #     projectiles_de_ciment.add(p)
            #     print("Cimenté!!!!!")
            # else:
                joueur1.rechargement = joueur1.rechargement - 50
                joueur1.compteur_de_tirs = joueur1.compteur_de_tirs + 1
                p = joueur1.tirer()
                projectiles.add(p)
            
    elif event.key == pygame.K_RETURN:
        if joueur2.rechargement >= 50:
            # if joueur2.compteur_de_tirs == 5:
            #     joueur2.rechargement = joueur2.rechargement - 50
            #     joueur2.compteur_de_tirs = joueur2.compteur_de_tirs - 5
            #     p = joueur2.tirer_ciment()
            #     projectiles_de_ciment.add(p)
            #     print("Cimenté!!!!!")
            # else:
                joueur2.rechargement = joueur2.rechargement - 50
                joueur2.compteur_de_tirs = joueur2.compteur_de_tirs + 1
                projectiles.add(joueur2.tirer())


# Main
def main():
    # Initialisation de la fenêtre d'affichage
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Jeu de tours")

    # Initialisation du système audio
    pygame.mixer.init(44100, -16, 2, 2048)

    # Groupes de sprites
    projectiles = pygame.sprite.Group()
    projectiles_de_ciment = pygame.sprite.Group()
    # Décor
    decor = Desert(ecran)
    

    # Création des joueurs
    joueur1 = init_joueur(1, "J1", 120, HAUTEUR_ECRAN - 200, Vecteur(40, 0), (0, 0, 255))
    joueur2 = init_joueur(2, "J2", LARGEUR_ECRAN - 120, HAUTEUR_ECRAN - 200, Vecteur(-40, 0), (255, 0, 0))

    # Timer
    clock = pygame.time.Clock()

    # Boucle d'évènements
    ingame = True

    while ingame:
        # Récupération des événements des joueurs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("On quitte")
                ingame = False
            elif event.type == pygame.KEYDOWN:
                gerer_action(event, joueur1, joueur2, projectiles,projectiles_de_ciment)

        #  DEBUT - Logique du jeu

        # Rechargement
        joueur1.gerer_rechargement()
        joueur2.gerer_rechargement()


        # Supprimer les projectiles sortis de l'écran
        s = [sprite for sprite in projectiles.sprites() if sprite.rect.centery >= HAUTEUR_ECRAN+50]
        projectiles.remove(s)  
        s = [sprite for sprite in projectiles_de_ciment.sprites() if sprite.rect.centery >= HAUTEUR_ECRAN+50]
        projectiles_de_ciment.remove(s)  

        #Supprimer les objets du décor sortis de l'écran
        s = [sprite for sprite in decor.projectiles.sprites() if sprite.rect.centery >= HAUTEUR_ECRAN+50]
        decor.projectiles.remove(s)

        # Test les collisions entre les projectiles et le décor
        decor.gerer_collisions(projectiles)

        # Test les collisions entre les projectiles et chaque joueur
        joueur1.gerer_degats(projectiles)
        joueur2.gerer_degats(projectiles)


        if joueur1.vie <= 0:
            print("Le joueur 2 gagne!!!")
            main()
        if joueur2.vie <= 0:
            print("Le joueur 1 gagne!!!")
            main()


        # Mettre à jour le décor
        decor.sprites.update()
        decor.projectiles.update()

      
        # Mettre à jour la position des projectiles
        projectiles.update()
        projectiles_de_ciment.update()

        # Mettre à jour l'état des joueurs
        joueur1.sprites.update()
        joueur2.sprites.update()

        #  FIN - Logique du jeu
        
        # Afficher le tout dans la fenêtre
        ecran.blit(decor.image, (0, 0))
        decor.sprites.draw(ecran)
        decor.projectiles.draw(ecran)
        projectiles.draw(ecran)
        projectiles_de_ciment.draw(ecran)
        #dessiner_croix(background, balle.rect.centerx, balle.rect.centery)
        joueur1.sprites.draw(ecran)
        joueur2.sprites.draw(ecran)
        pygame.display.flip()

        # 60 images / seconde
        clock.tick(60)


print("Programme principal")
if __name__ == '__main__':
    main()
