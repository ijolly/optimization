import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from telescope import Telescope
from math import sqrt
import tkinter as tk
import sys


# Global Variables Initial Values
iterations = 1000
overlap_weight = 2
distance_weight = 4
telescope_distance_weight = 1
n = 0
accumulator = list()
Telescopes = list()
area = 0
sum = 0
distance = 0
METHOD = "Nelder-Mead"
guess = np.array([0, 0])

# Create grid for plotting on
x, y = np.mgrid[-5:5:.05, -5:5:.05]
x = x.T
y = y.T

# Tinker Implementation for Inputting Fields

fields = 'Number of Telescopes', 'Overlap Weight', 'Distance Weight', 'Algorithm', 'Telescope Shape'


def Tiling(ents):
    # Adding in the telescopes to implement -> Random shape and size implementation
    # Ask for number of telescopes wanted ->
    # Take in inputs from tinker
    global sum
    global n
    global accumulator
    global Telescopes
    global overlap_weight
    global distance_weight
    global guess
    sum = 0
    guess = ([0, 0])
    Telescopes.clear()
    accumulator.clear()
    n = int(ents[int([y[0] for y in ents].index('Number of Telescopes'))][1].get())

    # Set's telescope sizing based on user input
    if(tkvar.get()=='Square'):
        setx = 5
        sety = 5
        seth = 3
        setw = 3
    elif(tkvar.get()=='Rectangle'):
        setx, sety = (5, 5)
        seth = 4
        setw = 2
    elif(tkvar.get()=='Random'):
        setx, sety = (random.randint(3, 5), random.randint(3, 5))
        seth = random.randint(2, 5)
        setw = random.randint(2, 5)

    for i in range(0, n):
        if(tkvar.get()=='Random'):
            setx, sety = (random.randint(3, 5), random.randint(3, 5))
            seth = random.randint(2, 5)
            setw = random.randint(2, 5)
        telescopex = setx #random.randint(3, 5)
        telescopey = sety #random.randint(3, 5)
        height = seth #random.randint(2, 5)
        width = setw #random.randint(2, 5)
        if(len(Telescopes) < n):
            Telescopes.append(Telescope(telescopex, telescopey, height, width, i))
        else:
            Telescopes.clear()
        print("Telescope", telescopex, telescopey, height, width, i)
    for i in range(0, n-1):
        guess = np.append(guess, 0)
        guess = np.append(guess, 0)

    # Define constants based on previous inputted values
    overlap_weight = float(ents[int([y[0] for y in ents].index('Overlap Weight'))][1].get())
    distance_weight = float(ents[int([y[0] for y in ents].index('Distance Weight'))][1].get())
    METHOD = algovar.get()

    # Defining the PLOT
    im = plt.imread("comet (1).png")
    # source -> https://www.nbcnews.com/mach/science/christmas-comet-back-another-visit-here-s-how-see-it-ncna949011

    # Create 1 figure: plot with the optimization path
    plt.figure(figsize=(7, 7))
    plt.clf()
    plt.axes([0, 0, 1, 1])

    contours = plt.contour(np.sqrt((x)**2 + (y)**2)*2,
                        extent=[-10, 10, -10, 10],
                        cmap=plt.cm.gnuplot)
    plt.clabel(contours,
            inline=1,
            fmt='%1.1f',
            fontsize=14)

    plt.axvline(0, color='k')
    plt.axhline(0, color='k')

    plt.text(-.9, 4.4, '$x_2$', size=20)
    plt.text(5.6, -.6, '$x_1$', size=20)


    plt.imshow(im, extent=[-10, 10, -10, 10])

    plt.axis('equal')
    plt.axis('off')

    # Optimization method
    optimize.minimize(f, guess, method=METHOD, constraints={"fun":constraint, "type":"eq"}, options={'maxiter': iterations, 'verbose': 3})

    accumulated = np.array(accumulator)
    plt.plot(accumulated[:, 0], accumulated[:, 1], linewidth=2)

    accum_lengt = len(accumulated) - 1
    # Dynamically printed Telescopes
    for n in range(len(Telescopes)):
        Telescopes[n].self_plot(accumulated[accum_lengt, n*2], accumulated[accum_lengt, n*2+1])

    plt.show()

    plt.imshow(im, extent=[-10, 10, -10, 10])
    print(area)
    print(distance)
    return None

def constraint(equation):
    return overlap_total(n, equation)

def area_overlap_coords(n1_centerx, n1_centery, n2_centerx, n2_centery, scope1, scope2):  # returns 0 if rectangles don't interact
    dx = min((scope1.width/2)+n1_centerx, (scope2.width/2)+n2_centerx) - max(n1_centerx - (scope1.width/2), n2_centerx - (scope2.width/2))
    dy = min((scope1.height/2)+n2_centery, (scope2.height/2)+n2_centery) - max(n1_centery - (scope1.height/2), n2_centery - (scope2.height/2))
    if (dx >= 0) and (dy >= 0):
        return dx*dy
    else:
        return 0


# Define as mathematical formula !!!!!!!!!!!
def area_overlap(a, b):  # returns None if rectangles don't interact
    dx = min(a.xmax, b.xmax) - max(a.xcoord, b.xcoord)
    dy = min(a.ymax, b.ymax) - max(a.ycoord, b.ycoord)
    if (dx >= 0) and (dy >= 0):
        return dx*dy
    else:
        return 0


def distance_between(x, y, a, b):
    return sqrt((x-a)**2 + (y-b)**2)


def overlap_total(n, equation): # Equation = [telescope[1].x, telescope[1].y, telescope[2].x, telescope[2].y,...]
    test = 0
    for i in range(n):
        for j in range(n):
            if j > i:
                test += overlap_weight * area_overlap_coords(equation[i*2], equation[(i*2)+1], equation[j*2], equation[(j*2)+1], Telescopes[i], Telescopes[j])
    return test

def max_overlap(n):
    test = 0
    for i in range(n):
        for j in range(n):
            if j > i:
                test += overlap_weight * area_overlap_coords(0, 0, 0, 0, Telescopes[i], Telescopes[j])
    return test

def normalized_overlap(n, equation):
    test = overlap_weight*overlap_total(n, equation)/max_overlap(n)
    return test


def distance_total(n, equation):
    test = 0
    for i in range(n):
        test += distance_weight * np.sqrt((equation[i*2]**2 + (equation[(i*2)+1])**2))
    return test


def distance_between_total(n, equation):
    test = 0
    for i in range(n):
        for j in range(n):
            if j > i:
                test += telescope_distance_weight * distance_between(equation[i*2], equation[(i*2)+1], equation[j*2], equation[(j*2)+1])
    return test

def total_area(n, equation):
    test = 0
    for i in range(n):
        test += Telescopes[i].tscope_area()
    return test



# Defining objective function f(x) = sqrt(ax^2+ay^2)+sqrt(bx^2+by^2)+10*area_overlap(a,b)
def f(equation):  # Define objective function
    global sum
    global area
    global distance
    global n
    global accumulator
    global guess

    area = overlap_total(n, equation)
    distance = distance_total(n, equation)
    distance_between = distance_between_total(n, equation)
    sum = distance_total(n, equation) + distance_between_total(n, equation) # #normalized_overlap(n, equation)
    print("Sum = {}, Area = {}, Distance = {}, Distance Between = {}, Equation = {}".format(sum, area, distance, distance_between, equation))
    accumulator.append(equation)
    print("Accumulator list length = {}".format(len(accumulator)))
    print("Percent Area Overlapping = {}\n".format((area/overlap_weight)/total_area(n, equation)/2))
    return sum

# GUI functions and INPUT below
def fetch(entries):
    print('%s: "%s"' % (entries[0][0], entries[0][1].get()))
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print('%s: "%s"' % (field, text))


def makeform(root, fields):
    global tkvar
    global algovar
    text = tk.Label(root)
    text.configure(text="Tiling")
    text.pack()
    #text2 = tk.Label(root)
    #text2.configure(text="Algorithm Options: Nelder-Mead, CG, BFGS, Powell")
    #text2.pack()
    entries = []

    # Below is the choices for the Algorithm
    algovar = tk.StringVar(root)
    algos = ('BFGS', 'CG', 'Powell', 'Nelder-Mead', 'SLSQP') # Maybe will have to change to list
    algovar.set('BFGS')

    # Below are choices for Telescope sizing
    tkvar = tk.StringVar(root)
    choices = ('Square','Rectangle','Random')
    tkvar.set('Square')

    # Create entry fields on UI
    for field in fields:
        if field=='Telescope Shape':
            row = tk.Frame(root)
            # popupMenu = tk.OptionMenu(row, tkvar, *choices)
            lab = tk.Label(row, width=17, text=field, anchor='w')
            ent = tk.OptionMenu(row, tkvar, *choices)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent))
            continue
        if field=='Algorithm':
            row = tk.Frame(root)
            # algoPopupMenu = tk.OptionMenu(row, algovar, *algos)
            lab = tk.Label(row, width=17, text=field, anchor='w')
            ent = tk.OptionMenu(row, algovar, *algos)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent))
            continue
        row = tk.Frame(root)
        lab = tk.Label(row, width=17, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries


root = tk.Tk()
ents = makeform(root, fields)
b1 = tk.Button(root, text='Display Tiling', command=(lambda: Tiling(ents)))
b1.pack(side=tk.LEFT, padx=5, pady=5)
b2 = tk.Button(root, text='Quit', command=root.quit)
b2.pack(side=tk.LEFT, padx=5, pady=5)
root.mainloop()
