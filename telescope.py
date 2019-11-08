import matplotlib.pyplot as plt


class Telescope:
    # Class to hold the telescope values.
    # Variables will be, bottom left coordinates, horizontal width, vertical height
    def __init__(self, x, y, h, w, id):
        self.xcoord = x
        self.ycoord = y
        self.height = h
        self.width = w
        self.id = id
        self.xmax = self.xcoord+self.width
        self.ymax = self.ycoord+self.height

    def center_point(self):
        return ((self.xcoord+self.width)/2, (self.ycoord+self.height)/2)

    def self_plot(self, x, y):
        self.xcoord = x-(self.width/2)
        self.ycoord = y-(self.height/2)

        plt.plot([self.xcoord, self.xcoord, self.xcoord+self.width, self.xcoord+self.width, self.xcoord],
                 [self.ycoord, self.ycoord+self.height, self.ycoord+self.height, self.ycoord, self.ycoord],
                 'k', linewidth=2)

        # Correctly fill out fill_between to show coverage between telescopes
        #plt.fill_between([self.xcoord, self.ycoord+self.height],
         #                [self.xcoord, self.ycoord],
          #               [self.xcoord+self.width, self.ycoord+self.height],
           #              color='.8')




        # Below is where the previous, stationary code is found
        # plt.plot([-1.5, -1.5,  1.5,  1.5, -1.5],
        #       [-1.5,  1.5,  1.5, -1.5, -1.5], 'k', linewidth=2)
        # plt.fill_between([-1.5,  1.5],
        #               [-1.5, -1.5],
        #              [1.5,  1.5],
        #             color='.8')
