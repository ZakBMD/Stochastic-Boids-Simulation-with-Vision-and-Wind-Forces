import math
import numpy as np
import random
import pygame
from vector import Vector,normalize_diff_angle

max_angle = math.pi / 3                             #Inisialisation de l'angle maximum de rotation pour éviter les retournements brusques
heading_wind = random.uniform(-1,1)*math.pi         #Inisiatlisation aléatoire de la direction du vent

class Boid:
    """
    A single simulated boid that can interact with its surroundings and act
    according to boids rules.
    """
    def __init__(self, pos, vel):
        "Initialisation du boid"
        self.position = pos                             #Position du boid
        self.velocity = vel                             #Vitesse du boid
        self.acceleration = Vector()                        #Accélération du boid
        self.max_speed = 10                                 #Vitesse maximale du boid
        self.size = 2                                           #Taille du boid
        self.heading = self.velocity.angle() + math.pi / 2      #Direction du boid
        self.color = (255, 255, 255)                            #Direction du boid


    def bounce(self, width, height):                
        "Modification pour prendre en compte le monde torique"
        if self.position.x > width:
            self.position.x = 0             #Passage à droite si le boid est trop à gauche
        if self.position.x < 0:
            self.position.x = width         #Passage à gauche si le boid est trop à droite
        if self.position.y > height:
            self.position.y = 0             #Passage en haut si le boid est trop en bas
        if self.position.y < 0:
            self.position.y = height        #Passage en bas si le boid est trop en haut


        
    def interact(self,d,v,n,coeff,optional):

        if optional == 1 :

            c_wind = 0.005

            "Ajout de la force du Vent"
            self.acceleration += c_wind * Vector(math.cos(heading_wind), math.sin(heading_wind))


        c_group,c_avoid,c_align = coeff                 #Séparation des coefficients des forces

        if n!=0:

            "Force de groupement"
            self.acceleration += c_group*d*(1/n) 

            "Force d' évitement"
            d_magni = d.magnitude()
            self.acceleration -= c_avoid*d*(1/(n*d_magni*d_magni)) 

            "Force d' alignement"
            self.acceleration += c_align*v*(1/n)

        else:
            "Force aléatoire si le boid n'a aucun voisin"
            self.acceleration += Vector(random.gauss(0, 0.4), random.gauss(0, 0.4))



    def update(self,dt,optional):
        if optional == 1 :
            previous_angle=self.velocity.angle()            #Conservation de l'angle à t

        self.velocity += self.acceleration * dt         #Actualisation de la vitesse à t+dt

        if self.velocity.magnitude() > self.max_speed:
            "Restriction à la vitesse maximale si ca dépasse"
            self.velocity = Vector(self.max_speed*math.cos(self.velocity.angle()),self.max_speed*math.sin(self.velocity.angle()))

        if optional == 1 :
            current_angle = self.velocity.angle()               #Conservation de l'angle à t+dt

            diff_angle = normalize_diff_angle(current_angle,previous_angle)         #Différence des angles normalisées

            "Restriction à l'angle maximal"
            if -diff_angle >= max_angle:                            #On regarde si le boid tourne trop vers la gauche
                new_angle=previous_angle - max_angle                #On lui applique la rotation maximale vers la gauche
                self.velocity = Vector(self.velocity.magnitude()*math.cos(new_angle),self.velocity.magnitude()*math.sin(new_angle))
            elif diff_angle >= max_angle:                           #On regarde si le boid tourne trop vers la droite
                new_angle=previous_angle + max_angle                #On lui applique la rotation maximale vers la droite
                self.velocity = Vector(self.velocity.magnitude()*math.cos(new_angle),self.velocity.magnitude()*math.sin(new_angle))
        
              
        self.position += self.velocity * dt         #Actualisation de la position à t+dt

        self.heading = self.velocity.angle() + math.pi / 2              #Actualisation de la direction (visuelle) à t+dt
        # reset acceleration
        self.acceleration = Vector()



    def rotation_2D(self, angle):
        ### NE PAS MODIFIER CETTE FONCTION ###
        return np.array(
            [
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)],
            ]
        )
    
    def draw(self, screen):
        ### NE PAS MODIFIER CETTE FONCTION ###
        size = 10
        # 2D triangle facing down
        points = [
            (0,-size),
            (size//2,size//2),
            (-size//2,size//2)
        ]
        rotated_points = []
        rot = self.rotation_2D(self.heading)
        rotated_points = (rot@np.array(points).T).T
        rotated_points = [
            tuple([p[0]+self.position.x, p[1]+self.position.y]) for p in rotated_points
        ]
        pygame.draw.polygon(screen, self.color, rotated_points, width=2)

    def __repr__(self):
        ### NE PAS MODIFIER CETTE FONCTION ###
        return f"Boid ({self.position.x:.1f}, {self.position.y:.1f})"