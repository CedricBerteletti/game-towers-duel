import pygame
from sprites import SpritePesant

class Projectile(SpritePesant):
    """
    Classe gérant un projectile.
    """

    def __init__(self):
        SpritePesant.__init__(self)
        self.degats = 10

class Boulet(Projectile):
    """
    Classe gérant un boulet.
    """

    TAILLE_BOULET = 20

    def __init__(self):
        SpritePesant.__init__(self)
        self.charger_png("boulet.png")
        self.image = pygame.transform.scale(self.image, (self.TAILLE_BOULET, self.TAILLE_BOULET))
        self.rect.width = self.TAILLE_BOULET
        self.rect.height = self.TAILLE_BOULET
        self.degats = 5

# class Boulet_de_ciment(Boulet):
#     TAILLE_BOULET_DE_CIMENT = 30
#     TAILLE_MUR_DE_CIMENT = 30

#     def __init__(self):
#         SpritePesant.__init__(self)
#         self.charger_png("boulet_de_ciment.png")
#         self.image = pygame.transform.scale(self.image, (self.TAILLE_BOULET_DE_CIMENT, self.TAILLE_BOULET_DE_CIMENT))
#         self.rect.width = self.TAILLE_BOULET_DE_CIMENT;
#         self.rect.height = self.TAILLE_BOULET_DE_CIMENT;
#         self.minuteur = 60
#         self.degats = 3
#         self.solidification = 0

    
#     def update(self):
#         SpritePesant.update(self)
#         self.position_x = self.rect.x
#         self.position_y = self.rect.y
#         self.minuteur = self.minuteur - 1       
#         if self.minuteur <= 0:
#             if self.solidification == 0:
#                 self.charger_png("mur_de_ciment.png")
#                 self.image = pygame.transform.scale(self.image, (self.TAILLE_MUR_DE_CIMENT, self.TAILLE_MUR_DE_CIMENT))
#                 self.rect.width = self.TAILLE_MUR_DE_CIMENT;
#                 self.rect.height = self.TAILLE_MUR_DE_CIMENT;
#                 self.gravite = 0
#                 self.rect.x  = self.position_x
#                 self.rect.y = self.position_y
#                 self._derniere_vitesse_init = (0.0, 0.0)
#                 self.solidification = 1
#                 self.init_mouvement
            
        
        

class Coco(Projectile):
    """
    Classe gérant une noix de coco.
    """

    TAILLE_NOIX = 30

    def __init__(self):
        SpritePesant.__init__(self)
        self.charger_png("noix_de_coco.png")
        self.image = pygame.transform.scale(self.image, (self.TAILLE_NOIX, self.TAILLE_NOIX))
        self.rect.width = self.TAILLE_NOIX
        self.rect.height = self.TAILLE_NOIX
        self.degats = 0
   
            
        
