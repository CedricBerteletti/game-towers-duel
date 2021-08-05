# coding: utf-8
"""
Module de gestion des joueurs
"""

import pygame
from sprites import Sprite, SpritePesant, Fleche, charger_son
from projectiles import Projectile, Boulet, Coco


MAX_VIE = 100
RECHARGEMENT_INITIAL = 0


class Joueur(object):
    """Classe pour gérer un joueur"""

    HAUTEUR_TOUR = 160
    LARGEUR_TOUR = 100

    def __init__(self, numero=1, nom="Joueur", x=0, y=0):
        """Constructeur : initialisation du joueur"""
        self.vie = MAX_VIE
        self.rechargement = RECHARGEMENT_INITIAL
        self.numero = numero
        self.nom = nom
        self._x = x
        self._y = y
        self.compteur_de_tirs = 0
        #self.tour = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        
        # Sprite du vecteur de tir
        self.tir = Fleche()

        # Sprite de la tour
        # Tour blanche de débogage
        # self.tour = Sprite()
        # self.tour.image = pygame.Surface([30, 60])        
        # self.tour.image.set_colorkey((0, 0, 0))
        # self.tour.image.fill((250, 250, 250))
        # self.tour.rect = self.tour.image.get_rect()
        # Tour image
        self.tour = Sprite()
        self.tour.charger_png("tour" + str(self.numero) + ".png")
        self.tour.image = pygame.transform.scale(self.tour.image, (self.LARGEUR_TOUR, self.HAUTEUR_TOUR))
        self.tour.rect.width = self.LARGEUR_TOUR
        self.tour.rect.height = self.HAUTEUR_TOUR

        # Sprite du nom
        font = pygame.font.Font(None, 28)
        text = font.render(self.nom, 1, (255, 255, 255))
        textpos = text.get_rect()
        sprite_name = Sprite()
        sprite_name.image = pygame.Surface((textpos.width, textpos.height))
        sprite_name.image.set_colorkey((0, 0, 0))        
        sprite_name.rect.centerx = self.x
        sprite_name.rect.y = 10
        sprite_name.image.blit(text, [0, 0])

        # Sprite de la barre de vie
        self._sprite_vie = None

        # Sprite de la barre de rechargement 

        self._sprite_rechargement = None

        # Ajout des sprites au groupe de sprites du joueur
        self.sprites.add(self.tir)
        self.sprites.add(self.tour)
        self.sprites.add(sprite_name)
        
        # Fin des initialisations
        self.x = x
        self.y = y
        self.__reinit_sprite_vie()
        self.__reinit_sprite_rechargement()


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.tir.rect.centerx = value
        self.__positionner_tour()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.tir.rect.centery = value
        self.__positionner_tour()


    def changer_angle(self, delta):
        self.tir.vecteur.theta = self.tir.vecteur.theta + delta
    

    def changer_force(self, delta):
        self.tir.vecteur.r = self.tir.vecteur.r + delta

    def __positionner_tour(self):
        # Pour tour blanche
        # self.tour.rect.centerx = self.x
        # self.tour.rect.y = self.y + 20
        # Pour tout canon
        if self.numero == 1:
            self.tour.rect.centerx = self.x - self.LARGEUR_TOUR/2 - 10
        else:
            self.tour.rect.centerx = self.x + self.LARGEUR_TOUR/2 + 10
        self.tour.rect.y = self.y - 10


    def __reinit_sprite_vie(self):
        # Si la barre de vie est existante, on la supprime
        if not (self._sprite_vie is None):
            self.sprites.remove(self._sprite_vie)
        
        self._sprite_vie = Sprite()
        self._sprite_vie.image = pygame.Surface([self.vie, 10])        
        self._sprite_vie.image.set_colorkey((0, 0, 0))
        if self.vie >= 80:
            self._sprite_vie.image.fill((0, 255, 0))
        elif self.vie >= 40:
            self._sprite_vie.image.fill((255, 255, 0))
        elif self.vie >= 20: 
            self._sprite_vie.image.fill((255, 128, 0))
        else:          
            self._sprite_vie.image.fill((155, 0, 0))
        self._sprite_vie.rect.x = self.x - MAX_VIE/2
        self._sprite_vie.rect.y = 30

        self.sprites.add(self._sprite_vie)
    
    def __reinit_sprite_rechargement(self):
        # Si la barre de vie est existante, on la supprime
        if not (self._sprite_rechargement is None):
            self.sprites.remove(self._sprite_rechargement)
            

        self._sprite_rechargement  = Sprite()
        self._sprite_rechargement.image = pygame.Surface([self.rechargement/2, 10])        
        self._sprite_rechargement.image.set_colorkey((0, 0, 0))
        
        if self.rechargement >= 200:
            self.rechargement = 200
            self._sprite_rechargement.image.fill((0, 0, 255))
        elif self.rechargement  >= 150:
            self._sprite_rechargement.image.fill((100, 200, 0))
        elif self.rechargement >= 100: 
            self._sprite_rechargement.image.fill((200, 100, 0))
        elif self.vie >= 50: 
            self._sprite_rechargement.image.fill((255, 50, 0))
        else:          
            self._sprite_rechargement.image.fill((255, 0, 0))
        
        self._sprite_rechargement.rect.x = self.x - MAX_VIE/2
        self._sprite_rechargement.rect.y = 45
        self.sprites.add(self._sprite_rechargement)
       
    def gerer_rechargement(self):
        self.rechargement = self.rechargement + 0.5
        self.__reinit_sprite_rechargement()


    def tirer(self):
        b = Boulet()
        b.rect.centerx = self.x
        b.rect.centery = self.y
        b.echelle = 1
        b.vitesse.x = self.tir.vecteur.x
        b.vitesse.y = self.tir.vecteur.y
        #b.afficher_vecteur_vitesse = True
        b.init_mouvement()
        son = charger_son("canon_01.wav")
        son.play()
        return b

    # def tirer_ciment(self):
    #     b = Boulet_de_ciment()
    #     b.rect.centerx = self.x
    #     b.rect.centery = self.y
    #     b.echelle = 1
    #     b.vitesse.x = self.tir.vecteur.x
    #     b.vitesse.y = self.tir.vecteur.y
    #     #b.afficher_vecteur_vitesse = True
    #     b.init_mouvement()
    #     son = charger_son("canon_01.wav")
    #     son.play()
    #     return b

    def gerer_degats(self, projectiles):
        # Si un projectile percute la tour d'un joueur, le projectile disparaît et
        # le joueur encaisse des dégâts
        supprimer_projectile = True
        projectiles_impacts = pygame.sprite.spritecollide(self.tour, projectiles, supprimer_projectile)
        for projectile_impact in projectiles_impacts:
            self.vie = self.vie - projectile_impact.degats
        if self.vie < 0:
            self.vie = 0
        
        self.__reinit_sprite_vie()
        