DEPLACEMENT = {0: "Stay", 1: "Left", 2: "Right"}


class TuringMachineCode:
    # initialise la machine de turing en prenant pour entrée
    # le nombre de ruban qui doit etre au moins de 1,
    # les transition [[q1,q2], [[[value1, value2], DEPLACEMENT]...]],
    # l'état initial et l'état final,
    # Les états doivent étre numèroté et un dictionnaire doit etre donnée dans
    # etat avec leur noms
    # le nombre de ruban doit etre superieur ou egal a 1
    def __init__(self, name):
        self.name = name

        self.init = None
        self.final = None
        self.etat_nombre = 0
        self.etat = {}
        self.etat_transi = []
        self.value = []
        self.deplacement = []
        self.ruban = []
        self.tete = []

    def ajout_etat(self, etat):
        self.etat[self.etat_nombre] = etat
        self.etat_nombre += 1
        return self.etat_nombre - 1

    def init_ruban(self, nombre_ruban):
        if len(self.ruban) == 0:
            for _ in range(nombre_ruban):
                self.ruban.append([[], []])
                self.tete.append([1, 0])
        elif len(self.ruban) != nombre_ruban:
            print("erreur dans la transition")

    def init_etat_initial(self, init):
        if self.init is None:
            inside = False
            for j in self.etat.keys():
                if init in self.etat[j]:
                    inside = True
                    self.init = j
            if not inside:
                self.init = self.ajout_etat(init)
        else:
            print("Init initialiser 2 fois")

    def init_final(self, final):
        if self.final is None:
            inside = False
            for j in self.etat.keys():
                if final in self.etat[j]:
                    inside = True
                    self.final = j
            if not inside:
                self.final = self.ajout_etat(final)
        else:
            print("Accept initialiser 2 fois")

    def init_transition_ruban(self, transition):
        couple = []
        for i in transition[0]:
            inside = False
            for j in self.etat.keys():
                if i == self.etat[j]:
                    inside = True
                    couple.append(j)
            if not inside:
                couple.append(self.ajout_etat(i))

        self.etat_transi.append(couple)
        self.value.append([])
        self.deplacement.append([])
        self.value[-1].append(transition[1][0])
        self.deplacement[-1].append(transition[1][1])

        self.init_ruban(len(transition[1]))

    def machine_turing_integrity(self):
        if self.init is None:
            print("No init define")
            return False
        if self.final is None:
            print("No accept state define")


if __name__ == '__main__':
    machine = TuringMachineCode("test")
    machine.init_etat_initial("init")
    machine.init_etat_initial("init2")
    machine.init_final("accept")
    machine.init_final("accept2")
    machine.init_transition_ruban([["q0", "q1"], [["1", "2"], "Right"]])
    print(machine.etat)
    print(machine.ruban, machine.etat_transi, machine.value, machine.tete)
    print(machine.etat_nombre, machine.value, machine.deplacement)
