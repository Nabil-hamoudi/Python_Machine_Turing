import sys
import argparse

DEPLACEMENT = ("<", ">", "-")


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
        self.machine_import_init = {}
        self.machine_import_fin = {}
        self.machine_objet = {}
        self.count_mt = 0

    def connect_machine(self, name, prec):
        second_etat = prec[0][1]
        prec[0][1] = self.etat[self.machine_import_init[name]]
        value_acc = []
        direction = []
        for i in prec[1]:
            value_acc.append(i[0][0])
            direction.append(i[1])
        value_rec = tuple(value_acc)
        direction = tuple(direction)
        info = self.init_transition_ruban([prec[0], [[[i, i], '-'] for i in value_rec]])
        if type(info) == str:
            return info
        second_etat = self.ajout_etat(second_etat)
        for i in self.etat_transi.keys():
            for j in self.etat_transi[i].keys():
                if self.etat_transi[i][j][0] == self.machine_import_fin[name]:
                    self.etat_transi[i][j] = (second_etat, self.etat_transi[i][j][1])

        self.machine_import_init = {}
        self.machine_import_fin = {}
        self.import_machine(self.machine_objet[name])

    def import_machine(self, machine):
        if type(machine) == str:
            return machine
        else:
            conversion = {}
            self.count_mt += 1
            add = '_' + str(self.count_mt)
            if machine.name in self.machine_import_init.keys():
                return "on ne peut pas importer la meme machine plusieurs fois"
            else:
                for i in machine.etat.keys():
                    num = self.ajout_etat(machine.etat[i] + add)
                    conversion[i] = num
                    if i == machine.init:
                        self.machine_import_init[machine.name] = num
                    elif i == machine.final:
                        self.machine_import_fin[machine.name] = num
                for i in machine.etat_transi.keys():
                    etat_tran = {}
                    for j in machine.etat_transi[i].keys():
                        value = machine.etat_transi[i][j]
                        etat_tran[j] = (conversion[value[0]], value[1])
                    self.etat_transi[conversion[i]] = etat_tran

                self.ruban = machine.ruban
                self.tete = machine.tete
        self.machine_objet[machine.name] = machine

    def change_name(self, name):
        self.name = name

    def ajout_etat(self, etat):
        for i in self.etat.keys():
            if etat == self.etat[i]:
                return i

        self.etat[self.etat_nombre] = etat
        self.etat_transi[self.etat_nombre] = {}
        self.etat_nombre += 1
        return self.etat_nombre - 1

    def init_etat_initial(self, init):
        if self.init is None:
            self.init = self.ajout_etat(init)
        else:
            return "Init initialiser 2 fois"

    def init_final(self, final):
        if self.final is None:
            self.final = self.ajout_etat(final)
        else:
            return "Accept initialiser 2 fois"

    def init_transition_ruban(self, transition):
        value_rec = []
        value_new = []
        direction = []
        for i in transition[1]:
            value_rec.append(i[0][0])
            value_new.append(i[0][1])
            if i[1] not in DEPLACEMENT:
                return (str(i[1]) + ' is an invalide argument for deplacement did you mean "<", ">" or "-"?')
            direction.append(i[1])

        value_rec = tuple(value_rec)
        value_new = tuple(value_new)
        direction = tuple(direction)

        if value_rec in self.etat_transi[self.ajout_etat(transition[0][0])].keys():
            return (str(transition[0][0]) + " error multiple possibility into value(s)" + str(value_rec))

        self.etat_transi[self.ajout_etat(transition[0][0])][value_rec] = (self.ajout_etat(transition[0][1]), (value_new, direction))

        nombre_ruban = len(transition[1])

        if len(self.ruban) == 0:
            for _ in range(nombre_ruban):
                self.ruban.append([])
                self.tete.append(0)
        elif len(self.ruban) != nombre_ruban:
            return str("le nombre de ruban de la transition ne match pas ceux des precedent")

    def machine_turing_integrity(self):
        if self.init is None:
            return "No init define"
        if self.final is None:
            return "No accept state define"

    # Crée une nouvelle instance de la machine de turing
    def instance_machine(self, word):
        ruban = []
        direction = []
        new = []
        for i in self.ruban:
            ruban.append(i.copy())
            direction.append(None)
            new.append(False)
        ruban[0] = [i for i in word]
        for field in ruban:
            if field == []:
                field.append("_")
        tete = self.tete.copy()
        etat = self.init
        return (ruban, tete, etat, direction, [], new)

    def mouvement(self, ruban, tete, etat):
        mouv_ruban = []
        mouv_direction_droite = []
        new = []
        if etat == self.final:
            return True
        transition = self.etat_transi[etat]
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
                                new.append(True)
                            else:
                                new.append(False)
                            mouv_ruban.append(i)
                            mouv_direction_droite.append(False)
                        case ">":
                            tete[i] += 1
                            if tete[i] == len(ruban[i]):
                                ruban[i].append("_")
                            new.append(False)
                            mouv_ruban.append(i)
                            mouv_direction_droite.append(True)
                        case "-":
                            new.append(False)
                            mouv_direction_droite.append(None)
                return (ruban, tete, etat, mouv_direction_droite, mouv_ruban, new)
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
                    info = machine.init_etat_initial(line[5:].strip())
                    if type(info) == str:
                        return ("line number: " + str(i + 1) + "\n" + info)
                elif line[:7] == "accept:":
                    info = machine.init_final(line[7:].strip())
                    if type(info) == str:
                        return ("line number: " + str(i + 1) + "\n" + info)
                elif line[:7] == "import:":
                    info = machine.import_machine(read_file(line[7:].strip()))
                    if type(info) == str:
                        return ("line number:" + str(i + 1) + "\n" + line[7:].strip() + '\n' + info)
                else:
                    line = str(line).split(",")
                    if '' in line:
                        return ("Comma at end or start of line " + str(i + 1))
                    if len(line) > 1:
                        prec = [[line[0].strip()], []]
                        for value in line[1:]:
                            prec[1].append([[value.strip()]])
                    else:
                        return ("Incorrect number of elements in line " + str(i + 1))

            else:
                line = str(line).split(",")
                if '' in line:
                    return ("Comma at end or start of line " + str(i + 1))
                if len(line) == (len(prec[1]) * 2) + 1 and line[1].strip() not in machine.machine_import_init.keys():
                    prec[0].append(line[0].strip())
                    for n, value in enumerate(line[1:(len(prec[1]) + 1)]):
                        prec[1][n][0].append(value.strip())
                    for n, value in enumerate(line[(len(prec[1]) + 1):]):
                        prec[1][n].append(value.strip())
                    info = machine.init_transition_ruban(prec)
                elif len(line) == (len(prec[1])) + 2 and line[1].strip() in machine.machine_import_init.keys():
                    prec[0].append(line[0].strip())
                    for n, value in enumerate(line[2:]):
                        prec[1][n].append(value.strip())
                    info = machine.connect_machine(line[1].strip(), prec)
                else:
                    return ("Incorrect number of elements in line " + str(i + 1))
                if type(info) == str:
                    return ("line number: " + str(i + 1) + "\n" + info)
                prec = None
    return machine


if __name__ == '__main__':
    AP = argparse.ArgumentParser()
    AP.add_argument('file', help='fichier contenant le code de la machine de turing', type=str)
    AP.add_argument('word', help='mot a entrée dans la machine de turing', type=str)
    args = AP.parse_args(sys.argv[1::])

    machine = read_file(args.file)

    if type(machine) == str:
        print(machine)
        sys.exit()

    value = machine.instance_machine(args.word)
    while type(value) == tuple:
        print(value[:3])
        value = machine.mouvement(value[0], value[1], value[2])
    print(value)
