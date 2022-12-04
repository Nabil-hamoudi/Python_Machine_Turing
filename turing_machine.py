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
        self.etat_transi = {}
        self.ruban = []
        self.tete = []

    def ajout_etat(self, etat):
        for i in self.etat.keys():
            if etat in self.etat[i]:
                return i

        self.etat[self.etat_nombre] = etat
        self.etat_transi[self.etat_nombre] = {}
        self.etat_nombre += 1
        return self.etat_nombre - 1

    def init_etat_initial(self, init):
        if self.init is None:
            self.init = self.ajout_etat(init)
            return True
        print("Init initialiser 2 fois")
        return False

    def init_final(self, final):
        if self.final is None:
            self.final = self.ajout_etat(final)
            return True
        print("Accept initialiser 2 fois")
        return False

    def init_transition_ruban(self, transition):
        value_rec = []
        value_new = []
        direction = []
        for i in transition[1]:
            value_rec.append(i[0][0])
            value_new.append(i[0][1])
            direction.append(i[1])

        value_rec = tuple(value_rec)
        value_new = tuple(value_new)
        direction = tuple(direction)

        if value_rec in self.etat_transi[self.ajout_etat(transition[0][0])].keys():
            print(transition[0][0], "error multiple possibility into value(s)", value_rec)
            return False

        self.etat_transi[self.ajout_etat(transition[0][0])][value_rec] = (self.ajout_etat(transition[0][1]), (value_new, direction))

        nombre_ruban = len(transition[1])

        if len(self.ruban) == 0:
            for _ in range(nombre_ruban):
                self.ruban.append([])
                self.tete.append([1, 0])
            return True
        elif len(self.ruban) != nombre_ruban:
            print("le nombre de ruban de la transition ne match pas ceux des precedent")
            return False
        return True

    def machine_turing_integrity(self):
        if self.init is None:
            print("No init define")
            return False
        if self.final is None:
            print("No accept state define")
            return False
        return True


class TuringMachineInstance(TuringMachineCode):
    def init_word(self, word):
        if self.machine_turing_integrity():
            for i in word:
                self.ruban.append(i)
            self.etat_actuel = self.init

    def mouvement(self):
        print(self.tete)
        print(self.ruban)


if __name__ == '__main__':
    machine = TuringMachineInstance("test")
    machine.init_etat_initial("qinit")
    machine.init_final("qaccept")
    machine.init_transition_ruban([["q0", "q1"], [[["1", "2"], "Right"], [["1", "2"], "Right"]]])
    machine.init_transition_ruban([["q0", "q1"], [[["1", "0"], "Right"]]])
    machine.init_transition_ruban([["q1", "q1"], [[["1", "1"], "Right"], [["1", "1"], "Right"]]])
    print(machine.etat_transi)
    print(machine.etat)
    print(machine.machine_turing_integrity())
    machine.mouvement()
