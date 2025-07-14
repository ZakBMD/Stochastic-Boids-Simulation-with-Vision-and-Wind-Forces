from math import sqrt, atan2, pi

def normalize_diff_angle(a, b):
    "Normalise la différence d'angle pour avoir un résultat entre -pi et pi"
    diff_angle = a-b
    return (diff_angle+pi) % (2*pi) - pi

class Vector:
    """
    A helper class to allow for easier manipulation of geometric data in 2D
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)
    
    def angle(self):
        # atan2 is always between -pi and pi
        return atan2(self.y, self.x)
   
    def distance_tore(self, other, width, height):
        d = other - self
        x1 = d.x
        x2 = width - x1
        y1 = d.y
        y2 = height - y1
        return Vector(min(x1, x2), min(y1, y2))
    
    def __add__(self, other):
        """
        Operator overload to allow for easy vector addition
        """
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise NotImplementedError("Vector can only added to other Vector")
    
    def __sub__(self, other):
        return self + (-other)
    
    def __neg__(self):
        return -1 * self
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(other * self.x, other * self.y)
        raise NotImplementedError("Vector can only be multiplied by a scalar")
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __repr__(self):
        return f"Vector ({self.x:.1f}, {self.y:.1f})"

