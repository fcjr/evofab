import cv2
from itertools import islice
from math import *

def calculate_perimeter(image):
    #copy the image as to not destroy it
    #image = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    #cv2.imshow("Image", image)

    # The first thing we are going to do is apply edge detection to
    # the image to reveal the outlines of the coins
    edged = cv2.Canny(blurred, 30, 150)
    #cv2.imshow("Edges", edged)

    # Find contours in the edged image.
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #sort them largest to smallest
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
    #print cnts[0]

    #calculate the peremiter
    #if there are no visible contours in the image, return a fitness of 0
    if len(cnts) == 0:
        return 0
    perimeter = cv2.arcLength(cnts[0], True)

    #downsample perimeter and draw on image
    cnts[0] = cnts[0][::10]
    

    #calculate turning angle
    pts = cnts[0][:]
    pts = [tuple(x[0]) for x in pts]
    for n in range(len(pts)-1):
        cv2.line(image, pts[n], pts[n+1], (0, 0, 0), 2, -1)
    angles = []
    for n,pt in islice(enumerate(pts), 0, None, 2):
        a1, a2 = [a - b for a,b in zip(pts[n], pts[n-1])]
        b1, b2 = [a - b for a,b in zip(pts[n+1], pts[n])]
        dot = a1*b1 + a2*b2
        angle = acos(round(dot/(sqrt(a1*a1 + a2*a2) * sqrt(b1*b1 + b2*b2)), 10))
        angle = angle * 180/pi
        angles.append(angle)
        #print n/2, "&", angle
    #bin_width = (max(angles) - min(angles))/10.0
    #print "\n"*5, bin_width

    #calculate PDF
    ###############
    bin_width = 7
    num_bins = int(floor((max(angles) - min(angles))/bin_width))
    PDF = []
    for x in range(num_bins + 1):
        l = min(angles) + (x * bin_width)
        r = min(angles) + ((x+1) * bin_width)
        num_in_range = 0
        for angle in angles:
            if angle > l and angle < r :
                num_in_range += 1
        PDF.append(num_in_range/float(len(angles)))
    
    for n,p in enumerate(PDF):
        print (min(angles) + (n * bin_width)), "&", (min(angles) + ((n+1)*bin_width)), "&", p

    #calculate entropy
    ##################
    e = 0
    for p in PDF:
        e += p * log(p, 10)
    e = -e
    print e
    #end

    color_interval = 255/len(cnts[0])
    for n,point in enumerate(cnts[0]):
        cv2.circle(image, (point[0][0], point[0][1]), 6, (0, 255-n*color_interval, 0), -1)
    cv2.imshow("EvoFab Evaluation", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    calculate_perimeter(cv2.imread("morph_compl/input.png"))
