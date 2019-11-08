import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from telescope import Telescope

# Check if there is a separate method of passing constraints to Nelder-Mead
# Create comma separated csv with Pandas.readcsv for test cases -> Dataframe

iterations = 50

x, y = np.mgrid[-5:5:.05, -5:5:.05]
x = x.T
y = y.T

# Adding in the telescopes to implement
n1 = Telescope(-1.5, -1.5, 3, 3, 1)
n2 = Telescope(5, 5, 3, 3, 2)
n3 = Telescope(4, 4, 2, 4, 3)

for i in (1, 2):
    # Create 2 figure: only the second one will have the optimization
    # path
    plt.figure(i, figsize=(7, 7))
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


# Define as mathematical formula !!!!!!!!!!!
def area_overlap(a, b):  # returns None if rectangles don't interact
    dx = min(a.xmax, b.xmax) - max(a.xcoord, b.xcoord)
    dy = min(a.ymax, b.ymax) - max(a.ycoord, b.ycoord)
    if (dx >= 0) and (dy >= 0):
        return dx*dy


# Defining objective function f(x) = sqrt(ax^2+ay^2)+sqrt(bx^2+by^2)+10*area_overlap(a,b)
def f(equation):  # Define objective function
    # Store the list of function calls
    accumulator.append(equation)
    return np.sqrt((equation[0])**2 + (equation[1])**2)


# Using the Nelder-Mead algorithm can be seen in the graph that is plotted
# f_prime(x) is not being used rn
#def f_prime(x):
 #   r = np.sqrt((x[0])**2 + (x[0])**2)
  #  return np.array(((x[0])/r, (x[0])/r))


optimize.minimize(f, np.array([5, 5]), method="Nelder-Mead", options={'maxiter': iterations})
                     # bounds=((-1.5, 1.5), (-1.5, 1.5))) # Used in the case of method="L-BFGS-B"

accumulated = np.array(accumulator)
plt.plot(accumulated[:, 0], accumulated[:, 1])

# Dynamically printed Telescope
n1.self_plot(accumulated[iterations, 0], accumulated[iterations, 1])

# Statically printed Telescope
n2.self_plot(2, 1)
# n3.self_plot(-3, -1)

plt.show()
print(area_overlap(n1, n2))
# print(accumulated[iterations, 0], accumulated[iterations, 1])
# print(x[0], y[0])
