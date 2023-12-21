from produit import Produit

class Parser:
    def __init__(self, chemin_fichier):
        self.chemin_fichier = chemin_fichier

        self.longueur_camion = 0
        self.largeur_camion = 0
        self.hauteur_camion = 0

        self.liste_produits = []
        self.parse_fichier()

    def parse_fichier(self):
        with open(self.chemin_fichier, 'r') as file:
            dimensions_camion = list(map(int, file.readline().split()))
            self.longueur_camion, self.largeur_camion, self.hauteur_camion = dimensions_camion

            nb_produits = int(file.readline())

            for _ in range(nb_produits):
                dimensions_produit = list(map(int, file.readline().split()))
                produit = Produit(*dimensions_produit)
                self.liste_produits.append(produit)

    def __str__(self):
        print(f"Dimensions du camion : {self.longueur_camion} x {self.largeur_camion} x {self.hauteur_camion}")
        print("Liste des produits :")
        for produit in self.liste_produits:
            print(produit)
        return ""

# if __name__ == "__main__":
#     chemin_fichier = 'input.sample'
#     parser = Parser(chemin_fichier)
#     print(parser)
