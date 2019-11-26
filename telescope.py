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
        self.centerx = (self.xcoord+self.width)/2
        self.centery = (self.ycoord+self.height)/2
        self.xleft = self.centerx-(self.width/2)
        self.xright = self.centerx+(self.width/2)
        self.ybottom = self.centery-(self.height/2)
        self.ytop = self.centery+(self.height/2)
        self.new_center_x = 0
        self.new_center_y = 0

    def center_point(self):
        return ((self.xcoord+self.width)/2, (self.ycoord+self.height)/2)

    def self_plot(self, x, y):
        self.xcoord = x-(self.width/2)
        self.ycoord = y-(self.height/2)

        plt.plot([self.xcoord, self.xcoord, self.xcoord+self.width, self.xcoord+self.width, self.xcoord],
                 [self.ycoord, self.ycoord+self.height, self.ycoord+self.height, self.ycoord, self.ycoord],
                 'w', linewidth=2)

    def moved_tscope(self, centerx, centery):
        self.centerx = centerx
        self.centery = centery
        nid = self.id
        return Telescope(self.xleft, self.ybottom, self.width, self.height, nid)

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
