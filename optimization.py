import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from telescope import Telescope
from math import sqrt

# Check if there is a separate method of passing constraints to Nelder-Mead
# Create comma separated csv with Pandas.readcsv for test cases -> Dataframe

# Global Variables
iterations = 500
overlap_weight = 2
distance_weight = 4
telescope_distance_weight = 1
area = 0
sum = 0
distance = 0
METHOD = "Nelder-Mead"
guess = np.array([5, 5, 5, 5, 5, 5, 5, 5])

# Create grid for plotting on
x, y = np.mgrid[-5:5:.05, -5:5:.05]
x = x.T
y = y.T

# Adding in the telescopes to implement -> Random shape and size implementation
# Ask for number of telescopes wanted ->
centers = []
Telescopes = []
n = int(input("How many telescopes do you want? "))
for i in range(0, n):
    Telescopes.append(Telescope(random.randint(3,5), random.randint(2, 5), random.randint(2, 5), random.randint(2, 5), i))


# n1 = Telescope(-1.5, -1.5, 3, 3, 1)
# n2 = Telescope(5, 5, 3, 3, 2)
# n3 = Telescope(4, 4, 3, 3, 3)

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


# Defining objective function f(x) = sqrt(ax^2+ay^2)+sqrt(bx^2+by^2)+10*area_overlap(a,b)
def f(equation):  # Define objective function
    # global sum
    # global area
    # global distance
    # for index in range(n):
    #     sum += distance_weight * np.sqrt((equation[index*2])**2 + (equation[index*2+1])**2)
    #     distance += distance_weight * np.sqrt((equation[index*2])**2 + (equation[index*2+1])**2)
    #
    # for i in range(n):
    #     for j in range(n):
    #         if j > i:
    #             sum += overlap_weight * area_overlap_coords(equation[i*2], equation[i*2+1], equation[j*2], equation[j*2+1], Telescopes[i], Telescopes[j])
    #             area += overlap_weight * area_overlap_coords(equation[i*2], equation[i*2+1], equation[j*2], equation[j*2+1], Telescopes[i], Telescopes[j])
    #
    # accumulator.append(equation)
    # return sum
    accumulator.append(equation)
    test = np.sqrt((equation[0]) ** 2 + (equation[1]) ** 2) + np.sqrt(equation[2] ** 2 + (equation[3] ** 2)) + \
           np.sqrt(equation[4] ** 2 + (equation[5] ** 2)) + overlap_weight * area_overlap_coords(equation[0],
                                                                                                 equation[1],
                                                                                                 equation[2],
                                                                                                 equation[3],Telescopes[0], Telescopes[1]) + \
           overlap_weight * area_overlap_coords(equation[0], equation[1], equation[4],
                                                equation[5], Telescopes[0], Telescopes[2]) + overlap_weight * area_overlap_coords(equation[2],
                                                                                                    equation[3],
                                                                                                    equation[4],
                                                                                                    equation[5], Telescopes[1], Telescopes[2]) + \
            telescope_distance_weight * distance_between(equation[0], equation[1], equation[2], equation[3]) + telescope_distance_weight * \
           distance_between(equation[0], equation[1], equation[4], equation[5]) + telescope_distance_weight * distance_between(equation[2], equation[3], equation[4], equation[5])
    return test


# Optimization method
optimize.minimize(f, guess, method="Nelder-Mead", options={'maxiter': iterations})

accumulated = np.array(accumulator)
plt.plot(accumulated[:, 0], accumulated[:, 1])

# Dynamically printed Telescopes
for n in range(len(Telescopes)):
    Telescopes[n].self_plot(accumulated[iterations, n*2], accumulated[iterations, n*2+1])

# n1.self_plot(accumulated[iterations, 0], accumulated[iterations, 1])
# n2.self_plot(accumulated[iterations, 2], accumulated[iterations, 3])
# n3.self_plot(accumulated[iterations, 4], accumulated[iterations, 5])

plt.show()
print(area)
print(distance)
