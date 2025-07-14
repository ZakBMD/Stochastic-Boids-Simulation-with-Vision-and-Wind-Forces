import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from flock import Flock

WIDTH = 1000
HEIGHT = 600
WINDOW_NAME = "Boids!"
BACKGRND_COLOR = (20, 20, 20)
temps_arret = 60    #Définition du temps d'arret de l'essai (en secondes)


"""
Valeur de préférence main.py 30 1 1 470 110 SEED? 0
Le coefficient d'évitement doit en effet être bien supérieur aux autres
"""


def run(detection_radius,alignment_weight,cohesion_weight,avoidance_weight,num_boids,seed,optional):
    #Rajout des autres arguments que num_boids
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)

    #Initialisation de Flock avec les nouveaux arguments
    flock = Flock(num_boids, WIDTH, HEIGHT,seed,(cohesion_weight,avoidance_weight,alignment_weight), detection_radius, optional)      

    run = True
    clock = pygame.time.Clock()
    framerate = 60

    # a pygame program follows this loop
    # while run : 
    #   check for game loop end
    #   tick for all objects
    #   draw all objects
    #   pygame update display

    if optional == 1:
        temps_ecoule=0                                          # Initialisation du temps écoulé

    while run:

        dt = clock.tick_busy_loop(framerate) / 30           # Diminution de la vitesse de visualisation de l'essai pour observer plus facilement
        
        for event in pygame.event.get():                    # Examine si un evenement s'est produit
            if event.type == pygame.QUIT:                   # Vérifie si l'on a quitté la simulation
                run = False                                     # Modifie la simulation pour qu'elle s'arrete au prochain tour de boucle
            if event.type == pygame.KEYDOWN:                # Vérifie si l'on a appuyé sur une touche
                if event.key == pygame.K_ESCAPE:                # Vérifie sque celle ci est la touche échap
                    run = False                                     # Modifie la simulation pour qu'elle s'arrete au prochain tour de boucle
        if optional == 1 :
            temps_ecoule += dt * 30 / 1000                  # Comptabilisation du temps ecoulé (en secondes)

            if temps_ecoule >= temps_arret:                 # Vérifie si l'on a terminé la simulation
                run = False                                     # Modifie la simulation pour qu'elle s'arrete au prochain tour de boucle

        
        screen.fill(BACKGRND_COLOR)
        flock.update(dt)
        flock.draw(screen)
        pygame.display.update()        # Affiche la simulation
        
    pygame.quit()        # Arrête la simulation
    exit()


def error_and_exit(message):
    print(f"Erreur: {message}", file=sys.stderr)
    print(
        f"\nUsage: {sys.argv[0]} num_boids\n"
        "\n"
        " num_boids: nombre de boids\n"
        "\n"
        f"exemple: {sys.argv[0]} 100\n"
        , file=sys.stderr
    )
    sys.exit(1)


def to_float(str):
    try:
        res = float(str)
    except ValueError:
        res = None
    return res


def read_argv():                            # Modification tel que le programme prend en compte la lecture des autres arguments
    if len(sys.argv) < 7:
        error_and_exit("Nombre d'arguments incorrect")
    detection_radius = int(sys.argv[1])
    alignment_weight = int(sys.argv[2])
    cohesion_weight = int(sys.argv[3])
    avoidance_weight = int(sys.argv[4])
    num_boids = int(sys.argv[5])
    seed = int(sys.argv[6])
    
    if len(sys.argv) == 7:
        optional =  0
    else:
        optional = int(sys.argv[7])

    return detection_radius,alignment_weight,cohesion_weight,avoidance_weight,num_boids,seed,optional

if __name__ == "__main__":
    detection_radius,alignment_weight,cohesion_weight,avoidance_weight,num_boids,seed,optional = read_argv()
    run(detection_radius,alignment_weight,cohesion_weight,avoidance_weight,num_boids,seed,optional)