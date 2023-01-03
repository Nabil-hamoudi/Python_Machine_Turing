import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import turing_machine

COULEUR_FOND = "black"

LARGEUR = 852
HAUTEUR = 100

TAILLE_SQUARE = 50
COLOR_SQUARE = "red"

PAUSE = 300
SPEED = 30
PIXEL_JUMP = 2.5

canvas = None

def deplacement(Right, ruban, mouvement=0):
    if mouvement < (TAILLE_SQUARE - PIXEL_JUMP):
        for i in ruban:
            for j in square[i]:
                if Right[i]:
                    canvas.move(j, -PIXEL_JUMP, 0)
                else:
                    canvas.move(j, PIXEL_JUMP, 0)
            for j in value[i]:
                if j is not None:
                    if Right[i]:
                        canvas.move(j, -PIXEL_JUMP, 0)
                    elif not Right[i]:
                        canvas.move(j, PIXEL_JUMP, 0)
        mouvement += PIXEL_JUMP
        canvas.after(SPEED, deplacement, Right, ruban, mouvement)
    else:
        for i in ruban:
            for j in square[i]:
                if Right[i]:
                    canvas.move(j, mouvement, 0)
                else:
                    canvas.move(j, -mouvement, 0)
            for j in value[i]:
                if j is not None:
                    if Right[i]:
                        canvas.move(j, -PIXEL_JUMP, 0)
                    elif not Right[i]:
                        canvas.move(j, PIXEL_JUMP, 0)
        mouvement = 0


def ruban_affichage(number):
    global fen, canvas, label_canvas, etat, square
    label_canvas = tk.Canvas(fen,
                             width=LARGEUR,
                             height=40,
                             bg=COULEUR_FOND)

    label_canvas.grid(row=0, column=0, columnspan=5)

    etat = label_canvas.create_text(LARGEUR / 2, 20,
                                    text="State: None",
                                    fill="#3156E1",
                                    font="Rockwell, 15")
    canvas = tk.Canvas(fen,
                       width=LARGEUR,
                       height=HAUTEUR*number,
                       bg=COULEUR_FOND)
    canvas.grid(row=1, column=0, columnspan=5)

    nombre_rectangle = LARGEUR / TAILLE_SQUARE
    square = []
    for j in range(number):
        x = (2 - TAILLE_SQUARE, 2)
        y = ((TAILLE_SQUARE / 2) + (j*HAUTEUR), (3 * (TAILLE_SQUARE / 2)) + (j*HAUTEUR))
        square.append([canvas.create_rectangle(x[0],
                                               y[0],
                                               x[1],
                                               y[1],
                                               fill=COLOR_SQUARE)])
        for i in range(round(nombre_rectangle) + 1):
            x = (2 + (TAILLE_SQUARE * i), 2 + TAILLE_SQUARE * (i+1))
            y = ((TAILLE_SQUARE / 2) + (j*HAUTEUR), (3 * (TAILLE_SQUARE / 2)) + (j*HAUTEUR))
            square[j].append(canvas.create_rectangle(x[0],
                                                     y[0],
                                                     x[1],
                                                     y[1],
                                                     fill=COLOR_SQUARE))
    square.reverse()


def update_etat(new_etat):
    label_canvas.itemconfig(etat, text="State: " + new_etat)


def value_update(ruban, tete, direction):
    for i, j in enumerate(tete):
        if direction[i] is None:
            correct_direction = 0
        elif direction[i]:
            correct_direction = -1
        else:
            correct_direction = 1
        if ruban[i][j+correct_direction] == '_':
            try:
                if value[i][j+correct_direction] is not None:
                    canvas.delete(value[i][j+correct_direction])
                    value[i][j+correct_direction] = None
            except IndexError:
                value[i].append(None)
        else:
            try:
                if value[i][j+correct_direction] is None:
                    value[i][j+correct_direction] = canvas.create_text(8.5*(TAILLE_SQUARE), ((len(ruban)-i)-0.5)*HAUTEUR, text=str(ruban[i][j+correct_direction]), fill="#303030", font="Rockwell, 30")
                else:
                    canvas.itemconfig(value[i][j+correct_direction], text=str(ruban[i][j+correct_direction]))
            except IndexError:
                value[i].append(canvas.create_text(8.5*(TAILLE_SQUARE), ((len(ruban)-i)-0.5)*HAUTEUR, text=str(ruban[i][j+correct_direction]), fill="#303030", font="Rockwell, 30"))


def machine_deroulement(output):
    if type(output) == bool:
        if output:
            mb.showinfo('etat', 'Accepter')
            return True
        else:
            mb.showinfo('etat', 'Rejeter')
            return False
    for i in range(len(value)):
        if output[5][i]:
            value[i].insert(0, None)
    deplacement(output[3], output[4])
    value_update(output[0], output[1], output[3])
    update_etat(machine_turing.etat[output[2]])
    output = machine_turing.mouvement(output[0], output[1], output[2])
    canvas.after((TAILLE_SQUARE//3 * SPEED) + PAUSE, machine_deroulement, output)


def start(word):
    if canvas is None:
        mb.showerror("APPLICATION_ERROR", "Pas de machine de turing initialiser")
        return False
    reset()
    output = machine_turing.instance_machine(word)
    value[0] = [canvas.create_text(((8.5 + i)*(TAILLE_SQUARE)), ((len(machine_turing.ruban)-0.5)*HAUTEUR), text=j, fill="#303030", font="Rockwell, 30") for i, j in enumerate(word)]
    machine_deroulement(output)


def reset():
    global value
    if canvas is not None:
        label_canvas.destroy()
        canvas.destroy()
    ruban_affichage(len(machine_turing.ruban))
    value = [[] for _ in range(len(machine_turing.ruban))]


def file_chargement():
    global machine_turing, value, canvas
    machine_turing = turing_machine.read_file(fd.askopenfilename())
    if type(machine_turing) == str:
        canvas = None
        mb.showerror('FILE_ERROR', machine_turing)
    else:
        reset()


fen = tk.Tk()

fen.title("Génération de terrain de jeu")
fen.config(bg=COULEUR_FOND)
fen.resizable(width=False, height=False)

bouton_file = tk.Button(fen, fg="red", bg="black", text="import a machine", command=file_chargement)
bouton_file.grid(row=2, column=4, padx=10, pady=10)

word_field = tk.Entry(fen, width=50, font='Rockwell, 15')
word_field.grid(row=2, column=0, padx=10, pady=10)

bouton_lancement = tk.Button(fen, fg="red", bg="black", text="START", command=lambda: start(word_field.get()))
bouton_lancement.grid(row=2, column=1, padx=10, pady=10)

fen.mainloop()
