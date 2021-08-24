import statistics
import cv2
import getpass
import imutils
import numpy as np
import os
import matplotlib.pyplot as plt
import getpass

from imutils import contours
from skimage import measure

IMAGE_PATH = '/home/'+getpass.getuser()+'/Pictures/Canon_700D/'

if not os.path.isdir(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)
        
        
isFatal = False



def calculate_mean(dataset):
    r = np.array(dataset["R"])
    g = np.array(dataset["G"])
    b = np.array(dataset["B"])
    luminance = np.array(dataset["Luminance"])
    mask_pixels = np.array(dataset["Mask_Pixels"])
    print("CHECK_0_1")
    mask_mean = None
    r_mean = np.mean(r)
    g_mean = np.mean(g)
    b_mean = np.mean(b)
    luminance_mean = np.mean(luminance)
    mask_pixels_mean = np.mean(mask_pixels)
    print("CHECK_0_1")
    return r_mean, g_mean, b_mean, luminance_mean, mask_pixels_mean


def mark_brightest_spots(image_src, nod,acc):
    mark_brightest_spots.data = {
        "Index": [],
        "Mask": [],
        "R": [],
        "G": [],
        "B": [],
        "Luminance": [],
        "Mask_Pixels": [],
        "isPassed": [],
        "X": [],
        "Y": []
    }

    isFatal = False
    ACCURACY = acc
    ACCURACY_MID = acc - 0.1
    ACCURACY_LOW = acc - 0.2


    i = 0
    image = image_src

    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.blur(gray, (30, 30))

    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    labels = measure.label(thresh, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")
    # loop over the unique components
    pixels_tab = list()
    for label in np.unique(labels):

        if label == 0:
            continue

        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)

        pixels_tab.append(numPixels)
    mean_pixels_num = statistics.mean(pixels_tab) * 0.2
    i = 0
    for label in np.unique(labels):
        mark_brightest_spots.data["Index"].append(i)
        # if this is the background label, ignore it
        if label == 0:
            i = i + 1
            continue

        # otherwise, construct the label mask and count the
        # number of pixels
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels >= mean_pixels_num:
            mask = cv2.add(mask, labelMask)
            mean = cv2.mean(image, labelMask)
            R = mean[2]
            G = mean[1]
            B = mean[0]
            brightness = (0.2126 * R + 0.7152 * G + 0.0722 * B)
            print(
                f"{i} => {(round(R, 1))}, {round(G, 1)}, {round(B, 1)} Luminance => {round(brightness, 1)}, number of pixels: {numPixels}")
            mark_brightest_spots.data["Mask"].append(labelMask)
            mark_brightest_spots.data["R"].append(R)
            mark_brightest_spots.data["G"].append(G)
            mark_brightest_spots.data["B"].append(B)
            mark_brightest_spots.data["Luminance"].append(brightness)
            mark_brightest_spots.data["Mask_Pixels"].append(numPixels)

            cnts = cv2.findContours(labelMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            for (k, c) in enumerate(cnts):
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)
                ((cX, cY), radius) = cv2.minEnclosingCircle(c)

                mark_brightest_spots.data["X"].append(cX)
                mark_brightest_spots.data["Y"].append(cY)

                cont = cv2.circle(image, (int(cX), int(cY)), 75,
                                  (0, 255, 0), 3)
                cv2.putText(image, "#{}".format(i), (x, y - 15),cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4)
            i += 1

    r_mean, g_mean, b_mean, luminance_mean, mask_pixels_mean = calculate_mean(mark_brightest_spots.data)

    mask_tab =  mark_brightest_spots.data["Mask"]
    r_tab =  mark_brightest_spots.data["R"]
    g_tab =  mark_brightest_spots.data["G"]
    b_tab =  mark_brightest_spots.data["B"]
    luminace_tab =  mark_brightest_spots.data["Luminance"]
    mask_pixels_tab =  mark_brightest_spots.data["Mask_Pixels"]


    isFatal = False 

    for i in range(0, len( mark_brightest_spots.data["R"])):
        isFatal = False
        mask_from_data = mask_tab[i]
        r_from_data = r_tab[i]
        g_from_data = g_tab[i]
        b_from_data = b_tab[i]
        luminace_from_data = luminace_tab[i]
        mask_pixels_from_data = mask_pixels_tab[i]

        print(
            f'{i+1} => {(np.absolute(r_mean - r_from_data) / r_from_data) * 100},{(np.absolute(g_mean - g_from_data) / g_from_data) * 100},{(np.absolute(b_mean - b_from_data) / b_from_data) * 100},')
      
        if luminace_from_data > (luminance_mean + (1-ACCURACY) * luminance_mean) or luminace_from_data < (luminance_mean - (1 - ACCURACY) * luminance_mean):
            print(f'illuminance not OK, illuminance is {luminace_from_data}, mean is {luminance_mean}')
            cnts = cv2.findContours(mask_from_data.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            for (k, c) in enumerate(cnts):
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)
                ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                cont = cv2.circle(image, (int(cX), int(cY)), 75,
                                  (255, 50, 0), 3)
            isFatal = True
           

        elif luminace_from_data > (luminance_mean + (1-ACCURACY_MID) * luminance_mean) or luminace_from_data < (luminance_mean - (1 - ACCURACY_MID) * luminance_mean):
            print(f'illuminance VERY not OK, illuminance is {luminace_from_data}, mean is {luminance_mean}')
            cnts = cv2.findContours(mask_from_data.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            for (k, c) in enumerate(cnts):
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)
                ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                cont = cv2.circle(image, (int(cX), int(cY)), 75,
                                  (0,230,255), 3)
            isFatal = True
            
        elif luminace_from_data > (luminance_mean + (1-ACCURACY_LOW) * luminance_mean) or luminace_from_data < (luminance_mean - (1 - ACCURACY_LOW) * luminance_mean):
            print(f'illuminance VERY not OK, illuminance is {luminace_from_data}, mean is {luminance_mean}')
            cnts = cv2.findContours(mask_from_data.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            for (k, c) in enumerate(cnts):
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)
                ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                cont = cv2.circle(image, (int(cX), int(cY)), 75,
                                  (0, 0, 255), 3)
            isFatal = True
        else:
            if mask_pixels_from_data > (mask_pixels_mean + (1-ACCURACY) * mask_pixels_mean) or mask_pixels_from_data < (mask_pixels_mean - (1 - ACCURACY) * mask_pixels_mean):
                print(f'radius of glow is  not OK, radius in pixel is {mask_pixels_from_data}, mean is {mask_pixels_mean}')

                cnts = cv2.findContours(mask_from_data.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                for (k, c) in enumerate(cnts):
                    # draw the bright spot on the image
                    (x, y, w, h) = cv2.boundingRect(c)
                    ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                    cont = cv2.circle(image, (int(cX), int(cY)), 75,
                                      (255, 50, 0), 3)
                isFatal = True
           
            elif mask_pixels_from_data > (mask_pixels_mean + (1 - ACCURACY_MID) * mask_pixels_mean) or mask_pixels_from_data < (mask_pixels_mean - (1 - ACCURACY_MID) * mask_pixels_mean):
                print(f'radius of glow is  not OK, radius in pixel is {mask_pixels_from_data}, mean is {mask_pixels_mean}')

                cnts = cv2.findContours(mask_from_data.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                for (k, c) in enumerate(cnts):
                    # draw the bright spot on the image
                    (x, y, w, h) = cv2.boundingRect(c)
                    ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                    cont = cv2.circle(image, (int(cX), int(cY)), 75,
                                      (0, 230, 255), 3)
                isFatal = True
                

            elif mask_pixels_from_data > (mask_pixels_mean + (1-ACCURACY_LOW) * mask_pixels_mean) or mask_pixels_from_data < (mask_pixels_mean - (1 - ACCURACY_LOW) * mask_pixels_mean):
                print(f'radius of glow is VERY not OK, radius in pixel is {mask_pixels_from_data}, mean is {mask_pixels_mean}')

                cnts = cv2.findContours(mask_from_data.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                for (k, c) in enumerate(cnts):
                    # draw the bright spot on the image
                    (x, y, w, h) = cv2.boundingRect(c)
                    ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                    cont = cv2.circle(image, (int(cX), int(cY)), 75,
                                      (0,0, 255), 3)
                isFatal = True
           
        
            

        if isFatal == False:
            mark_brightest_spots.data["isPassed"].append(True)
        else:
            mark_brightest_spots.data["isPassed"].append(False)
    if i+1 != int(nod):
        not_enough = int(nod)-(i+1)
        isFatal = True
    else:
        not_enough = 0
    # cnts = contours.sort_contours(cnts)[0]
    # loop over the contours

    # for (i, c) in enumerate(cnts):
    #     # draw the bright spot on the image
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     ((cX, cY), radius) = cv2.minEnclosingCircle(c)
    #     cont = cv2.circle(image, (int(cX), int(cY)), 150,
    #                       (0, 0, 255), 3)
    #     cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)



    if not os.path.exists(IMAGE_PATH):
        os.mkdir(IMAGE_PATH)
    cv2.imwrite(IMAGE_PATH + os.path.basename(image_src), image)
    cv2.waitKey(0)
    return IMAGE_PATH + os.path.basename(image_src), isFatal, not_enough

# mark_brightest_spots(IMAGE_PATH + 'PIC_29-09-20--14:35:08.jpg')
def return_data():
    return  mark_brightest_spots.data
