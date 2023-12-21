class Produit:
    def __init__(self, longueur, largeur, hauteur):
        self.longueur = longueur
        self.largeur = largeur
        self.hauteur = hauteur
        self.length = longueur * largeur * hauteur

    def __str__(self):
        return f"Produit({self.longueur}, {self.largeur}, {self.hauteur})"
