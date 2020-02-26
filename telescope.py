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
                 'w', linewidth=2, label="id = {} width = {} height = {}".format(self.id, self.width, self.height))
        plt.text(self.xcoord, self.ycoord, self.id, bbox=dict(facecolor='red',alpha=0.5))
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)

    def moved_tscope(self, centerx, centery):
        self.centerx = centerx
        self.centery = centery
        nid = self.id
        return Telescope(self.xleft, self.ybottom, self.width, self.height, nid)

    def tscope_area(self):
        return self.width * self.height
