from detect import Detect
from box import Box
from rand_coord import coordinates
from PIL import Image

# Get Image Data
bbox, dimensions = Detect()
W = dimensions[0]
H = dimensions[1]
ar = (4,5)


RPT_MAX = 10
best = None

### Random Restart Algorithm
for i in range(RPT_MAX):
    curr = Box(coordinates(W=W, H=H, ar=ar))
    neighbors = curr.GetNeighbors()

    # Steepest-ascent
    for neighbor in neighbors:
        # minimize cost function
        if neighbor.Cost() < curr.Cost():
            curr = neighbor
    
    if best is None or curr.Cost() < best.Cost():
        best = curr

# Crop Function
def Crop():
    im = Image.open("images/test.jpg")
    im_cropped = im.crop((best.x1, best.y1, best.x2, best.y2))
    width, height = best.x2 - best.x1, best.y2 - best.y1
    print(f'Width = {width}, Height = {height}')
    im_cropped.show()
    im_cropped.save("images/cropped.jpg")

Crop()