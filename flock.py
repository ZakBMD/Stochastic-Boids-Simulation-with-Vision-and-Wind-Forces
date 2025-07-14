import random 
from boid import Boid
from vector import Vector, normalize_diff_angle
from math import pi

view_angle = pi / 1.5          #Angle de vision du boid (ici il ne voit plus derrière lui)

class Flock:
    """
    Initial paper available at https://dl.acm.org/doi/pdf/10.1145/37402.37406
    A bit more details here https://www.red3d.com/cwr/boids/
    A flock of boids holding the general parameters and for loops to run the
    simulation.
    """
    def __init__(self, num_boids, width, height,seed,coeff,detection_radius,optional):
        self.num_boids = num_boids                  # Nombre de boids sur le terrain
        self.boids = []                             # Liste des boids sur le terrain
        self.width = width                          # Largeur du terrain
        self.height = height                        # Hauteur du terrain
        "Conservation des autres arguments"
        self.seed=seed                              # Seed de la simulation
        self.coeff=coeff                            # Coefficient de la simulation
        self.detection_radius = detection_radius    # Coefficient du rayon de detecion des boids
        "Conservation de l'argument pour les ajouts facultatif"
        self.optional = optional

        "Mise en place de la seed donné"
        random.seed(self.seed)                

        # Initialize random boids
        for _ in range(num_boids):
            pos_x = random.randint(0, self.width)               # Position X aléatoire sur le terrain
            pos_y = random.randint(0, self.height)              # Position Y aléatoire sur le terrain
            pos = Vector(pos_x, pos_y)                          # Création du vecteur position
            vel_x = random.gauss(0, 1)                          # Vitesse X aléatoire sur le terrain
            vel_y = random.gauss(0, 1)                          # Vitesse Y aléatoire sur le terrain
            vel = Vector(vel_x, vel_y)                          # Création du vecteur vitesse
            self.boids.append(Boid(pos, vel))                   # Ajout du boid à la liste des boids

        if self.optional == 1 :
            (self.boids)[0].color=(255,255,0)                     # Initialisation d'un boid pour la visualisation et pouvoir le suivre (Version facultative)
            print(" Visualisation du projet facultatif")
        else :
            (self.boids)[0].color=(0,255,255)                     # Initialisation d'un boid pour la visualisation et pouvoir le suivre (Version obligatoire)
            print(" Visualisation du projet obligatoire")



    def detect(self,boid,detection_radius):
        """
        Programme de détection des boids alentours (de facon conique si optional==1) et création d'un ensemble regroupant ces derniers
        """
        neighbour=set()
        for other in self.boids:

            d = boid.position.distance_tore(other.position, self.width, self.height)            #Vecteur Distance entre boid et other
            
            if 0<d.magnitude()<detection_radius:
                if self.optional == 1 :
                    "Prise en compte dans le cône de vision"
                    diff_angle = abs(normalize_diff_angle(boid.velocity.angle(), d.angle()))            #Différence des angles normalisées en valeur absolue
                    if diff_angle < view_angle:
                        "Ajout du voisin dans le rayon de détection du cone de vision"
                        neighbour.add(other)
                else:
                    "Ajout du voisin dans le rayon de détection"
                    neighbour.add(other)
        return neighbour
    


    def update(self, dt):
        for boid in self.boids:
            """
            Met à jour la position et les vitesses de tous les boids en fonction de leurs interactions en fournissant des données à interact
            """
            neighbour=self.detect(boid,self.detection_radius)
            n = len(neighbour)
            for other in neighbour:
                d = boid.position.distance_tore(other.position, self.width, self.height)        #Vecteur Distance entre boid et other
                
                "Prise en compte de de l'interaction entre boid et other (on lui fournit la distance, la vitesse et les coefficients des forces)"
                boid.interact(d, other.velocity, n, self.coeff, self.optional)

        for boid in self.boids:
            """
            Met à jour la position de tous les boids pour gérer les rebonds des boids lorsqu'ils atteignent les bords de la simulation
            """
            boid.bounce(self.width, self.height)
                
        for boid in self.boids:
            """
            Met à jour les boids dans le temps
            """
            boid.update(dt, self.optional)
        

    def draw(self, screen):
        ### NE PAS MODIFIER CETTE FONCTION ###
        for boid in self.boids:
            boid.draw(screen)
