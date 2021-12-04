from abc import ABC, abstractmethod

class Element(ABC):
    def __init__(self, element):
        self.element = element

    @abstractmethod
    def bonus(self,element):
        pass

class Feu(Element):
    def __init__(self):
        super().__init__("feu")

    def bonus(self,element):
        if element.element == "plante": return 1.2
        elif element.element == "eau": return 0.8
        else: return 1 

class Plante(Element):
    def __init__(self):
        super().__init__("plante")

    def bonus(self,element):
        if element.element == "eau": return 1.2
        elif element.element == "feu": return 0.8
        else: return 1 

class Eau(Element):
    def __init__(self):
        super().__init__("eau")

    def bonus(self,element):
        if element.element == "feu": return 1.2
        elif element.element == "plante": return 0.8
        else: return 1 

class Pokemon(Element):
    def __init__(self,nom,pv,attaque,defense):
        self.nom = nom
        self.pv = pv
        self.pv_max = pv
        self.attaque = attaque
        self.defense = defense
        self.niveau = 1
        self.xp = 0
        self.xp_next = 5

    def add_xp(self, adv):
        diff = adv.niveau - self.niveau
        if(diff > 0):
            self.xp += round((2 + self.niveau/2) + diff)
        else: self.xp += round(2 + self.niveau/2)
        if(self.xp > self.xp_next):
            self.level_up()

    def xp_next_up(self):
        self.xp_next = round(self.xp_next * 1.4)

    def heal(self):
        self.pv = self.pv_max

    def attaquer(self,autre):
        multiplicater = self.bonus(autre)
        print(f"Le multiplicateur vaut {multiplicater}!")
        print(f"Attaque de base: {str(self.attaque)}\nAttaque après multiplicateur {str(round(self.attaque*multiplicater))}\n")
        degats = round((4+self.attaque)*multiplicater)-autre.defense
        if(degats<0):
            degats = 0
        elif(degats>autre.pv):
            autre.pv = 0
        else:
            autre.pv-=degats

    def level_up(self):
        self.niveau+=1
        self.attaque_up()
        self.defense_up()
        self.pv_up()
        self.xp_next_up()

    def get_name(self):
        return self.nom

    def __str__(self):
        return f'{self.nom}: pv {self.pv}, attaque: {self.attaque}, defense: {self.defense}, niveau: {self.niveau}'

    @abstractmethod
    def attaque_up(self):
        pass

    @abstractmethod
    def defense_up(self):
        pass

    @abstractmethod
    def pv_up(self):
        pass  

class Bulbizar(Pokemon, Plante):
    def __init__(self):
        Pokemon.__init__(self,"Bulbizar",25,6,4)
        Plante.__init__(self)

    def attaque_up(self):
        self.attaque+=1

    def defense_up(self):
        self.defense+=2

    def pv_up(self):
        self.pv_max+=3

    def print(self):
        print(f"Nom: {self.nom}, pv: {self.pv}, attaque: {self.attaque}, def: {self.defense}, element: {self.element} ")

class Salameche(Pokemon, Feu):
    def __init__(self):
        Pokemon.__init__(self,"Salameche",25,4,6)
        Feu.__init__(self)

    def attaque_up(self):
        self.attaque+=2

    def defense_up(self):
        self.defense+=2

    def pv_up(self):
        self.pv_max+=3

    def print(self):
        print(f"Nom: {self.nom}, pv: {self.pv}, attaque: {self.attaque}, def: {self.defense}, element: {self.element} ")

class Carapuce(Pokemon, Eau):
    def __init__(self):
        Pokemon.__init__(self,"Carapuce",20,5,6)
        Eau.__init__(self)

    def attaque_up(self):
        self.attaque+=2

    def defense_up(self):
        self.defense+=4

    def pv_up(self):
        self.pv_max+=4

    def print(self):
        print(f"Nom: {self.nom}, pv: {self.pv}, attaque: {self.attaque}, def: {self.defense}, element: {self.element} ")

class Tournoi():
    def __init__(self, pokelist):
        self.pokelist = pokelist
        self.score = {}

    def start(self):
        choice = str(input("Quel type de tournoi voulez-vous? [R]éel / [S]imulation"))
        for poke1 in self.pokelist:
            print(poke1)
            for poke2 in self.pokelist:
                print(poke2)
                if(poke1 != poke2):
                    if(choice == "R" or choice == "r"):
                        reel = Combat_reel(poke1,poke2)
                        winner = reel.fight()
                        if(winner.get_name() in self.score):
                            self.score[winner.get_name()] = self.score.get(winner.get_name(),0) + 1  
                        else:
                            self.score[winner.get_name()] = 1
                    
                    elif(choice == "S" or choice == "s"):
                        sim = Combat_sim(poke1,poke2)
                        winner = sim.fight()
                        if(winner.get_name() in self.score):
                            self.score[winner.get_name()] = self.score.get(winner.get_name(),0) + 1  
                        else:
                            self.score[winner.get_name()] = 1

                    else: self.start(poke1,poke2)

        print(self.score)
       
class Combat(ABC):
    def __init__(self,pokelist):
        self.pokelist = pokelist

    @abstractmethod
    def fight(self,pokelist):
        pass

class Combat_sim(Combat):
    def __init__(self,poke1,poke2):
        super().__init__([poke1,poke2])

    def fight(self):
        defense, attaque = self.pokelist[0], self.pokelist[1]
        winner = attaque
        while(poke1.pv > 0 and poke2.pv > 0):
            print(f"{attaque.get_name()} attaque {defense.get_name()}")
            attaque.attaquer(defense)
            if(defense.pv <= 0):
                winner = attaque
                print(f"Le gagnant est {winner.get_name()}")
                print(f"{winner.pv}")
            attaque, defense = defense, attaque
        attaque.heal()
        defense.heal()
        print(f"Les deux Pokémon ont récupérés leur vie!")
        return winner

class Combat_reel(Combat):
    def __init__(self,poke1,poke2):
        super().__init__([poke1,poke2])

    def fight(self):
        #print(self.pokelist[0].__str__())
        defense, attaque = self.pokelist[0], self.pokelist[1]
        winner = attaque
        while(poke1.pv > 0 and poke2.pv > 0):
            print(f"{attaque.get_name()} attaque {defense.get_name()}")
            attaque.attaquer(defense)
            if(defense.pv <= 0):
                winner = attaque
                print(f"Le gagnant est {winner.get_name()}")
            attaque, defense = defense, attaque
        winner.add_xp(defense)
        return winner




poke1 = Bulbizar()
poke1.print()
poke2 = Carapuce()
poke2.print()
poke3 = Salameche()
poke3.print()
listpoke = []
listpoke.append(poke1)
listpoke.append(poke2)
listpoke.append(poke3)
tournoi = Tournoi(listpoke)
tournoi.start()
