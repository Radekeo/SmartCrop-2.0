from cmath import inf
from random import randint
from rand_coord import coordinates
from detect import Detect

bbox, dimensions = Detect()
W = dimensions[0]
H = dimensions[1]

class Box:
    def __init__(self, coord):
        self.x1, self.y1, self.x2, self.y2 = coord
        self.c = ((self.x2+self.x1)/2, (self.y2+self.y1)/2)
        self.w = self.x2 - self.x1
        self.h = self.y2 - self.y1

    '''
    define neighbors as all possible boxes with the same dimension within the image, 
    e.g if box dimension is 90 * 160, get all possible 90 * 160 boxes within the image
    '''
    def GetNeighbors(self):
        neighbors = set()
        neighbors.add(self)

        # neighbors is set of 30 random self.w * self.h boxes
        rand = 1
        while rand <= 30:
            new_x1 = self.x1
            while new_x1 == self.x1:
                new_x1 = randint(0, W-self.w)
                new_x2 = new_x1 + self.w

            new_y1 = self.y1
            while new_y1 == self.y1:
                new_y1 = randint(0, H-self.h)
                new_y2 = new_y1 + self.h
            
            neighbor = Box([new_x1, new_y1, new_x2, new_y2])

            rand += 1

        return neighbors

    def Cost(self):
        others = (Box(bbox), Box([0,0,W,H]))
        # Nearnes to center
        c_dist = self.CenterDistance(others[0])

        # Distance from detected object boundaries
        obj_dist = 0

        for i, d in enumerate(self.BorderDistance(others[0])):

            # cropper coordinates falling outside the bounding box should have more value
            # x1 and y1 values of the cropper should be less than x1 and x2 values of the detected object
            # negative distance values remain negative since cost function will be using min value
            if i == 0 or i == 2:
                obj_dist += d

            # x2 and y2 of the cropper should be higher than x2 and y2 of the detected object
            # x2 and y2 of the cropper should be positive, positive distances will have become negative
            # making positive values stronger as cost function will use min value
            if i == 1 or i == 3:
                obj_dist += -d

        # Nearness to outer edges
        edge_dist = 0

        for d in self.BorderDistance(others[1]):
            edge_dist += abs(d)
        
        # total cost
        cost = (3 * edge_dist) + (1.5 * c_dist) + obj_dist

        return cost

    def BorderDistance(self,other):
        x1_dist = self.x1 - other.x1
        x2_dist = self.x2 - other.x2
        y1_dist = self.y1 - other.y1
        y2_dist = self.y2 - other.y2

        dist = [x1_dist, x2_dist, y1_dist, y2_dist]

        return dist

    def CenterDistance(self, other):
        # for center distance, negativity or positivity if distances don't affect the value
        cx_dist = abs(self.c[0] - other.c[0])
        cy_dist = abs(self.c[1] - other.c[1])

        dist = cx_dist + cy_dist
        # print(f'Cropper center is {self.c} and Distance to roi center is {dist}') ### Debugging
        return dist