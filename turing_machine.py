import sys
import argparse

DEPLACEMENT = ("<", ">", "-")

# valeur correspondant a l'activation ou non des optimisation de machine de turing
SIMPLIFICATION_ACTIVE = True
##################################################################################

class TuringMachineCode:
    # initialise la machine de turing en prenant pour entrée
    # les transition [[q1,q2], [[[value1, value2], DEPLACEMENT]...]],
    # l'état initial et l'état final,
    # Les machine correspondant aux importation
    # Les états sont numèroté et un dictionnaire est donnée entre les numero et leur noms
    # le nombre de ruban doit etre superieur ou egal a 1

    def __init__(self):
        """
        Initialise les valeur de base
        """
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
        """
        connect une machine a partir du nom de celle ci
        et les valeur de la transition
        cette fonction crée une nouvelle transition
        entre l'état reconnaissant et une copie de la machine importé
        et entre la copie de la machine importé et le 2eme etat de la transition
        """
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
        del self.machine_import_init[name]
        del self.machine_import_fin[name]
        self.import_machine(self.machine_objet[name])

    def import_machine(self, machine):
        """
        ajoute toute les transition de la machine importé machine
        dans cette machine definit par import:
        """
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
        """
        change le nom de la machine de turing
        """
        self.name = name

    def ajout_etat(self, etat):
        """
        prend en entrée un etat en str
        et ressors son numero
        """
        for i in self.etat.keys():
            if etat == self.etat[i]:
                return i

        self.etat[self.etat_nombre] = etat
        self.etat_transi[self.etat_nombre] = {}
        self.etat_nombre += 1
        return self.etat_nombre - 1

    def init_etat_initial(self, init):
        """
        initialiser l'etat initial defini par init:
        """
        if self.init is None:
            self.init = self.ajout_etat(init)
        else:
            return "Init initialiser 2 fois"

    def init_final(self, final):
        """
        initialiser l'etat final defini par accept:
        """
        if self.final is None:
            self.final = self.ajout_etat(final)
        else:
            return "Accept initialiser 2 fois"

    def init_transition_ruban(self, transition):
        """
        Initialise les transition des rubans dans la machine de turing
        """
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
        """
        Verifie l'integrité d'une machine de turing
        et si elle peut s'éxécuter
        """
        if self.init is None:
            return "No init define"
        if self.final is None:
            return "No accept state define"
        if SIMPLIFICATION_ACTIVE:
            self.simplification()
        return self

    def simplification(self):
        """
        Simplification des transition
        """
        simplifie_transi = None
        for etat_init in self.etat_transi.keys():
            for reco_value in self.etat_transi[etat_init].keys():
                etat_fin = self.etat_transi[etat_init][reco_value][0]
                value_fin = self.etat_transi[etat_init][reco_value][1][0]
                deplacement = self.etat_transi[etat_init][reco_value][1][1]
                stay = True
                for i in deplacement:
                    if i != '-':
                        stay = False
                for i in range(len(value_fin)):
                    if reco_value[i] != value_fin[i]:
                        stay = False
                if etat_fin == self.final:
                    stay = False
                if stay:
                    simplifie_transi = (etat_init, reco_value, etat_fin)
        if simplifie_transi is None:
            return True
        # nouvel etat final, value_final, direction
        if self.etat_transi[simplifie_transi[2]] != {}:
            new_transi = (self.etat_transi[simplifie_transi[2]][simplifie_transi[1]][0],
                          self.etat_transi[simplifie_transi[2]][simplifie_transi[1]][1][0],
                          self.etat_transi[simplifie_transi[2]][simplifie_transi[1]][1][1])
            self.etat_transi[simplifie_transi[0]][simplifie_transi[1]] = (new_transi[0], (new_transi[1], new_transi[2]))
        else:
            del self.etat_transi[simplifie_transi[0]][simplifie_transi[1]]
        self.simplification()

    def instance_machine(self, word):
        """
        Cree une nouvelle instance de la machine de turing
        avec un mot
        """
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
        """
        effectue les mouvement de la machine un par un
        """
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
    """
    Lit un fichier contenant le code d'une machine de turing et genere un nouvel objet TuringMachineCode
    """
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
    machine = machine.machine_turing_integrity()
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
