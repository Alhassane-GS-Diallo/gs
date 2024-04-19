from datetime import datetime, timedelta
import uuid

print("---Bienvenue!---\n")
class cours :
    def __init__(self,titre,format):
        self.titre = titre
        self.format = format
        
class video(cours):
    def __init__(self,titre,format,dure):
        super().__init__(titre,format)
        self.dure = dure
    
    def afficher_info(self):
        print(f"Titre: {self.titre} \nFormat {self.format} \nDurée {self.dure} minutes ")

class pdf(cours):
    def __init__(self,titre,format,taille):
        super().__init__(titre,format)
        self.taille = taille
    def afficher_info(self):
        print(f"Titre: {self.titre} \nFormat {self.format} \nTaille {self.taille} Mo")
class client :
    def __init__(self):
        print("Bienvenue! Veuillez vous inscrire pour accéder aux cours.")
        self.nom = input("Entrez votre nom :")
        self.prenom = input("Entrez votre prénom :")
        self.idenfiant = self.generer_idenfiant()
        self.inscrit = False
        self.date_inscription = None   
        self.a_payer = False
        self.cours_achetes = []
    
    def generer_idenfiant(self):
        return f"{self.nom.lower()}_{self.prenom.lower()}_{uuid.uuid4().hex[:8]}"
    
    
    def s_inscrire(self):
        self.inscrit = True
        self.date_inscription = datetime.now()
        print(f"{self.nom} {self.prenom} s'est inscrit avec succès!\nIdentifiant :{self.idenfiant}")
        
    
    def generer_code(self):
        if self.inscrit:
            return f"Code d'accès : {self.nom}{self.idenfiant}"
        else:
            return "Le client doit d'abord s'inscrire pour avoir un code d'accès."
        
    def effectuer_paiement(self,moyenn_de_paiement):
        self.moyenn_de_paiement = int(input("Entrez votre numero de carte :"))
        if self.inscrit:
            if (datetime.now() - self.date_inscription).days >= 30 and not self.a_payer :
                if self.valider_moyen_paiement(moyenn_de_paiement):
                    print(f"Paiement effectué avec succès pour {self.nom} {self.prenom}")
                    self.a_payer = True
                else:
                    print("Moyen de paiemment invalide. Le paiement n'a été éffectué.")
            elif self.a_payer:
                print("Le client a déja payé.")
            else:
                print("Pas besoin de paiement pour le moment.")
        else:
            print("Le client doit d'abord s'inscrire pour pouvoir payer.")
    def valider_moyen_paiement(self,moyenn_de_paiement):
        if len(moyenn_de_paiement) == 9 and moyenn_de_paiement.isdigit():
            print("Le moyen de paiement est validé.")
            return True
        else:
            print("Le moyen de paiement est invalide. Assurez vous d'entrer un numero de cate de credit valide .")
            return False
client1 = client()
client1.s_inscrire()
print(client1.generer_code())

client1.effectuer_paiement(111111111)
client1.valider_moyen_paiement('123456789')
print("\n30 jours plus tard, veuillez effectuer votre paiement pour continuer à accéder aux cours.")
print("\nMerci d'avoir utiliser notre programme. Au revoir!")      
        
print("\t__--_--_--__"*5)
