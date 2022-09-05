from random import randint

def coordinates(W, H, ar):
    invalid = True

    while invalid:
        ## get 2 points on the x-axis at random, x2 > x1
        x1 = x2 = 0
        while x1 == x2:
            x1 = randint (0, W)
            x2 = randint (0, W)

        ## width (distance between both points on the x-axis)
        width = abs(x2 - x1)
       
        # get height using width and aspect ratio
        height = int((width/ar[0]) * ar[1])

        if height <= H:
            if x1 > x2:
                x1,x2 = x2, x1
            invalid = False 

    ## get a random point on the y axis
    y1 = randint(0, H-height)

    # get another point on the y axis using y1 and the height
    y2 = y1 + height
    coord = [x1, y1, x2, y2]
    
    return coord