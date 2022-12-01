DEPLACEMENT = {0: "Stay", 1: "Left", 2: "Right"}


class TuringMachineCode:
    # initialise la machine de turing en prenant pour entrée
    # le nombre de ruban qui doit etre au moins de 1,
    # les transition [((q1,q2), [((value1, value2), DEPLACEMENT)...])...],
    # l'état initial et l'état final,
    # Les états doivent étre numèroté et un dictionnaire doit etre donnée dans
    # etat avec leur noms
    # le nombre de ruban doit etre superieur ou egal a 1
    def __init__(self, name):
        self.name = name

        self.final = []
        self.etat = {}
        self.etat_transi = []
        self.value = []
        self.deplacement = []
        self.ruban = []
        self.tete = []

    def init_ruban(self, nombre_ruban):
        if len(self.ruban) == 0:
            for _ in range(nombre_ruban):
                self.ruban.append([[], []])
                self.tete.append([1, 0])
        elif len(self.ruban) != nombre_ruban:
            print("erreur dans la transition")

    def init_etat_initial(self, init):
        if self.init is None:
            self.init = init
        else:
            print("Init initialiser 2 fois")

    def init_final(self, final):
        self.final.append(final)

    def init_transition_ruban(self, transition):
        self.etat_transi.append(transition[0])
        self.value.append([])
        self.deplacement.append([])

        for j in transition[1]:
            self.value[-1].append(j[0])
            self.deplacement[-1].append(j[1])

        self.init_ruban(len(transition[1]))

    def machine_turing_integrity(self):
        if self.init is None:
            print("No init define")



class InstanceMachineTuring(TuringMachineCode):
    # initialise une instance d'une
    # machine de turing défini précédement
    def __init__(self, path, word):
        pass
