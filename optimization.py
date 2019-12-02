import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from telescope import Telescope
from math import sqrt
import tkinter as tk


# Global Variables Initial Values
iterations = 500
overlap_weight = 2
distance_weight = 4
telescope_distance_weight = 1
area = 0
sum = 0
distance = 0
METHOD = "Nelder-Mead"

# Guess here is allowing for max of 15 telescopes
guess = np.array([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])


# Create grid for plotting on
x, y = np.mgrid[-5:5:.05, -5:5:.05]
x = x.T
y = y.T

# Tinker Implementation for Inputting Fields

fields = 'Number of Telescopes', 'Algorithm', 'Overlap Weight', 'Distance Weight'


def fetch(entries):
    print('%s: "%s"' % (entries[0][0], entries[0][1].get()))
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print('%s: "%s"' % (field, text))


def makeform(root, fields):
    text = tk.Label(root)
    text.configure(text="Tiling")
    text.pack()
    text2 = tk.Label(root)
    text2.configure(text="Algorithm Options Nelder-Mead, GC, BFGS, others...")
    text2.pack()
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries


root = tk.Tk()
ents = makeform(root, fields)
b1 = tk.Button(root, text='Show', command=(lambda e=ents: fetch(e)))
b1.pack(side=tk.LEFT, padx=5, pady=5)
b2 = tk.Button(root, text='Quit', command=root.quit)
b2.pack(side=tk.LEFT, padx=5, pady=5)
root.mainloop()

# Adding in the telescopes to implement -> Random shape and size implementation
# Ask for number of telescopes wanted ->
# Take in inputs from tinker
centers = []
Telescopes = []
n = int(ents[int([y[0] for y in ents].index('Number of Telescopes'))][1].get())
for i in range(0, n):
    telescopex = random.randint(3, 5)
    telescopey = random.randint(3, 5)
    height = random.randint(2, 5)
    width = random.randint(2, 5)
    Telescopes.append(Telescope(telescopex, telescopey, height, width, i))
    print("Telescope", telescopex, telescopey, height, width, i)


# Define constants based on previous inputted values
overlap_weight = int(ents[int([y[0] for y in ents].index('Overlap Weight'))][1].get())
distance_weight = int(ents[int([y[0] for y in ents].index('Distance Weight'))][1].get())
METHOD = ents[int([y[0] for y in ents].index('Algorithm'))][1].get()

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
# fig, ax = plt.subplots()
# x = range(10)
plt.imshow(im, extent=[-10, 10, -10, 10])

plt.axis('equal')
plt.axis('off')

# And now plot the optimization path
accumulator = list()


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


def overlap_total(n, equation):
    test = 0
    for i in range(n):
        for j in range(n):
            if j > i:
                test += overlap_weight * area_overlap_coords(equation[i*2], equation[(i*2)+1], equation[j*2], equation[(j*2)+1], Telescopes[i], Telescopes[j])
    return test


def distance_total(n, equation):
    test = 0
    for i in range(n):
        test += distance_weight * np.sqrt((equation[i*2]**2 + (equation[(i*2)+1])**2))
    return test


# Defining objective function f(x) = sqrt(ax^2+ay^2)+sqrt(bx^2+by^2)+10*area_overlap(a,b)
def f(equation):  # Define objective function
    global sum
    global area
    global distance
    # for index in range(n):
    #     sum += distance_weight * np.sqrt((equation[index*2])**2 + (equation[index*2+1])**2)
    #     distance += distance_weight * np.sqrt((equation[index*2])**2 + (equation[index*2+1])**2)
    #
    # for i in range(n):
    #     for j in range(n):
    #         if j > i:
    #             sum += overlap_weight * area_overlap_coords(equation[i*2], equation[i*2+1], equation[j*2], equation[j*2+1], Telescopes[i], Telescopes[j])
    #             area += overlap_weight * area_overlap_coords(equation[i*2], equation[i*2+1], equation[j*2], equation[j*2+1], Telescopes[i], Telescopes[j])

    area = overlap_total(n, equation)
    distance = distance_total(n, equation)
    sum = distance_total(n, equation)

    accumulator.append(equation)
    return sum
    # accumulator.append(equation)
    # test = np.sqrt((equation[0]) ** 2 + (equation[1]) ** 2) + np.sqrt(equation[2] ** 2 + (equation[3] ** 2)) + \
    #        np.sqrt(equation[4] ** 2 + (equation[5] ** 2)) + overlap_weight * area_overlap_coords(equation[0],
    #                                                                                              equation[1],
    #                                                                                              equation[2],
    #                                                                                              equation[3],Telescopes[0], Telescopes[1]) + \
    #        overlap_weight * area_overlap_coords(equation[0], equation[1], equation[4],
    #                                             equation[5], Telescopes[0], Telescopes[2]) + overlap_weight * area_overlap_coords(equation[2],
    #                                                                                                 equation[3],
    #                                                                                                 equation[4],
    #                                                                                                 equation[5], Telescopes[1], Telescopes[2]) + \
    #         telescope_distance_weight * distance_between(equation[0], equation[1], equation[2], equation[3]) + telescope_distance_weight * \
    #        distance_between(equation[0], equation[1], equation[4], equation[5]) + telescope_distance_weight * distance_between(equation[2], equation[3], equation[4], equation[5])
    # return test


# Optimization method
optimize.minimize(f, guess, method=METHOD, options={'maxiter': iterations, 'verbose': 3})

accumulated = np.array(accumulator)
plt.plot(accumulated[:, 0], accumulated[:, 1], linewidth=2)

# Dynamically printed Telescopes
for n in range(len(Telescopes)):
    Telescopes[n].self_plot(accumulated[iterations, n*2], accumulated[iterations, n*2+1])

plt.show()
# plt.text(-2, -2, "CG", fontsize=20, bbox=dict(facecolor='red',alpha=0.5))
plt.imshow(im, extent=[-10, 10, -10, 10])
print(area)
print(distance)


