class Camion:
    def __init__(self, longueur, largeur, hauteur):
        self.longueur = longueur
        self.largeur = largeur
        self.hauteur = hauteur
        self.matrice = [[[0 for _ in range(hauteur)] for _ in range(largeur)] for _ in range(longueur)]
        self.produits = []

    def placer_produit(self, produit, x1, y1, z1, x2, y2, z2):
        length = len(self.produits) + 1
        for x in range(x1, x2):
            for y in range(y1, y2):
                for z in range(z1, z2):
                    self.matrice[x][y][z] = length
        self.produits.append(produit)

    def __str__(self):
        for z in range(self.hauteur):
            for y in range(self.largeur):
                for x in range(self.longueur):
                    print(self.matrice[x][y][z], end=" ")
                print()
            print()
        return f"Camion({self.longueur}, {self.largeur}, {self.hauteur})"