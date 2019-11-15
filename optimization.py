import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from telescope import Telescope

# Check if there is a separate method of passing constraints to Nelder-Mead
# Create comma separated csv with Pandas.readcsv for test cases -> Dataframe

# Global Variables
iterations = 500
overlap_weight = 0.5

# Create grid for plotting on
x, y = np.mgrid[-5:5:.05, -5:5:.05]
x = x.T
y = y.T

# Adding in the telescopes to implement -> Currently Static
n1 = Telescope(-1.5, -1.5, 3, 3, 1)
n2 = Telescope(5, 5, 3, 3, 2)
n3 = Telescope(4, 4, 3, 3, 3)


# Create 1 figure: plot with the optimization path
plt.figure(figsize=(7, 7))
plt.clf()
plt.axes([0, 0, 1, 1])

contours = plt.contour(np.sqrt((x)**2 + (y)**2),
                    extent=[-5, 5, -5, 5],
                    cmap=plt.cm.gnuplot)
plt.clabel(contours,
        inline=1,
        fmt='%1.1f',
        fontsize=14)

plt.axvline(0, color='k')
plt.axhline(0, color='k')

plt.text(-.9, 4.4, '$x_2$', size=20)
plt.text(5.6, -.6, '$x_1$', size=20)
plt.axis('equal')
plt.axis('off')

# And now plot the optimization path
accumulator = list()


def area_overlap_coords(n1_centerx, n1_centery, n2_centerx, n2_centery):  # returns None if rectangles don't interact
    dx = min((n1.width/2)+n1_centerx, (n2.width/2)+n2_centerx) - max(n1_centerx - (n1.width/2), n2_centerx - (n2.width/2))
    dy = min((n1.height/2)+n2_centery, (n2.height/2)+n2_centery) - max(n1_centery - (n1.height/2), n2_centery - (n2.height/2))
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


# Defining objective function f(x) = sqrt(ax^2+ay^2)+sqrt(bx^2+by^2)+10*area_overlap(a,b)
def f(equation):  # Define objective function
    # a, b = equation
    # Store the list of function calls in accumulator
    accumulator.append(equation)
    return np.sqrt((equation[0])**2 + (equation[1])**2) + np.sqrt(equation[2]**2 + (equation[3]**2)) + \
           np.sqrt(equation[4]**2 + (equation[5]**2)) + overlap_weight * area_overlap_coords(equation[0], equation[1], equation[2], equation[3]) + \
           overlap_weight * area_overlap_coords(equation[0], equation[1], equation[4], equation[5]) + overlap_weight * area_overlap_coords(equation[2], equation[3], equation[4], equation[5])


# Using the Nelder-Mead algorithm can be seen in the graph that is plotted
# f_prime(x) is not being used rn
#def f_prime(x):
 #   r = np.sqrt((x[0])**2 + (x[0])**2)
  #  return np.array(((x[0])/r, (x[0])/r))

# Optimization method
optimize.minimize(f, np.array([5, 5, 5, 5, 5, 5]), method="Nelder-Mead", options={'maxiter': iterations})

accumulated = np.array(accumulator)
plt.plot(accumulated[:, 0], accumulated[:, 1])

# Dynamically printed Telescopes
n1.self_plot(accumulated[iterations, 0], accumulated[iterations, 1])
n2.self_plot(accumulated[iterations, 2], accumulated[iterations, 3])
n3.self_plot(accumulated[iterations, 4], accumulated[iterations, 5])

plt.show()
print(area_overlap(n1, n2))
