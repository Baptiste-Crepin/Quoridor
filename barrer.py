import pygame

pygame.init()
largeur = 800
hauteur = 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Exemple d'Input")

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                continuer = False
            if event.key == pygame.K_a:
                print("La touche A a été enfoncée")

    pygame.display.flip()

pygame.quit()
