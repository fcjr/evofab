import cv2
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
    print cnts[0]

    #calculate the peremiter
    #if there are no visible contours in the image, return a fitness of 0
    if len(cnts) == 0:
        return 0
    perimeter = cv2.arcLength(cnts[0], True)

    #downsample perimeter and draw on image
    cnts[0] = cnts[0][::10]
    for point in cnts[0]:
        cv2.circle(image, (point[0][0], point[0][1]), 6, (0, 255, 0), -1)
    cv2.imshow("EvoFab Evaluation", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    calculate_perimeter(cv2.imread("input.png"))
