import sys
import argparse
import curses
from curses import wrapper


class TuringMachineCode:
    # initialise la machine de turing en prenant pour entrée
    # le nombre de ruban qui doit etre au moins de 1,
    # les transition [[q1,q2], [[[value1, value2], DEPLACEMENT]...]],
    # l'état initial et l'état final,
    # Les états doivent étre numèroté et un dictionnaire doit etre donnée dans
    # etat avec leur noms
    # le nombre de ruban doit etre superieur ou egal a 1
    def __init__(self):
        self.name = "Untitled"
        self.init = None
        self.final = None
        self.etat_nombre = 0
        self.etat = {}
        self.etat_transi = {}
        self.ruban = []
        self.tete = []

    def change_name(self, name):
        self.name = name

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
        print("Init initialiser 2 fois", end=" ")
        return False

    def init_final(self, final):
        if self.final is None:
            self.final = self.ajout_etat(final)
            return True
        print("Accept initialiser 2 fois", end=" ")
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
            print(transition[0][0], "error multiple possibility into value(s)", value_rec, end=" ")
            return False

        self.etat_transi[self.ajout_etat(transition[0][0])][value_rec] = (self.ajout_etat(transition[0][1]), (value_new, direction))

        nombre_ruban = len(transition[1])

        if len(self.ruban) == 0:
            for _ in range(nombre_ruban):
                self.ruban.append([])
                self.tete.append(0)
            return True
        elif len(self.ruban) != nombre_ruban:
            print("le nombre de ruban de la transition ne match pas ceux des precedent", end=" ")
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


def instance_machine(machine, word):
    ruban = machine.ruban.copy()
    ruban[0] = [i for i in word]
    for field in ruban:
        if field == []:
            field.append("_")
    tete = machine.tete.copy()
    etat = machine.init
    value = (ruban, tete, etat)
    while type(value) == tuple:
        print(value)
        value = mouvement(machine, value[0], value[1], value[2])
    print(value)


def mouvement(machine, ruban, tete, etat):
    if etat == machine.final:
        return True
    transition = machine.etat_transi[etat]
    rec = []
    rec = [field[tete[i]] for i, field in enumerate(ruban)]
    rec = tuple(rec)
    for i in transition.keys():
        if rec == i:
            etat = transition[rec][0]
            for i, value in enumerate(transition[rec][1][0]):
                ruban[i][tete[i]] = value
                match transition[rec][1][1][i]:
                    case "<":
                        tete[i] -= 1
                        if tete[i] == -1:
                            tete[i] = 0
                            ruban[i].insert(0, "_")
                    case ">":
                        tete[i] += 1
                        if tete[i] == len(ruban[i]):
                            ruban[i].append("_")
                    case "-":
                        pass
            return (ruban, tete, etat)
    return False


def read_file(path):
    f = open(path, "r")
    lines = f.readlines()
    machine = TuringMachineCode()

    prec = None
    for i, line in enumerate(lines):
        line = line.lstrip().rstrip('\n')
        if line != '' and line[:2] != '//':
            if prec is None:
                if line[:5] == "name:":
                    machine.change_name(line[5:].strip())
                elif line[:5] == "init:":
                    if not machine.init_etat_initial(line[5:].strip()):
                        print("line number: ", i)
                        return False
                elif line[:7] == "accept:":
                    if not machine.init_final(line[7:].strip()):
                        print("line number: ", i)
                        return False
                else:
                    line = str(line).split(",")
                    if len(line) > 1:
                        prec = [[line[0].strip()], []]
                        for value in line[1:]:
                            prec[1].append([[value.strip()]])
                    else:
                        print("Incorrect number of elements in line", i)
                        return False

            else:
                line = str(line).split(",")
                if len(line) == (len(prec[1]) * 2) + 1:
                    prec[0].append(line[0].strip())
                    for n, value in enumerate(line[1:(len(prec[1]) + 1)]):
                        prec[1][n][0].append(value.strip())
                    for n, value in enumerate(line[(len(prec[1]) + 1):]):
                        prec[1][n].append(value.strip())
                else:
                    print("Incorrect number of elements in line", i)
                    return False
                machine.init_transition_ruban(prec)
                prec = None
    return machine


if __name__ == '__main__':
    AP = argparse.ArgumentParser()
    AP.add_argument('file', help='fichier contenant le code de la machine de turing', type=str)
    AP.add_argument('word', help='mot a entrée dans la machine de turing', type=str)
    args = AP.parse_args(sys.argv[1::])
    machine = read_file(args.file)
    if not machine:
        sys.exit()

    instance_machine(machine, args.word)
