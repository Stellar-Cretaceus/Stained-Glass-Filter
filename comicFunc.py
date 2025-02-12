import cv2
import numpy as np
import global_var
from utils import Choose_Filter,errorwindow,nothing,ResizeWithAspectRatio

def createTrackBar():

    global_var.Trackbar_flag = 1

    cv2.namedWindow("Trackbar")
    cv2.resizeWindow("Trackbar", 300, 350) 
    cv2.createTrackbar("Threshold1", "Trackbar", 40, 255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbar", 40, 255, nothing)
    cv2.createTrackbar("Boldness", "Trackbar", 3, 20, nothing)

    cv2.createTrackbar("R", "Trackbar", 100, 200, nothing)
    cv2.createTrackbar("G", "Trackbar", 100, 200, nothing)
    cv2.createTrackbar("B", "Trackbar", 100, 200, nothing)

    cv2.createTrackbar('Brightness',
                    'Trackbar', 300, 2 * 255,
                    BrightnessContrast)
    cv2.createTrackbar('Contrast', 'Trackbar',
                    161, 2 * 127,
                    BrightnessContrast) 
    
def BrightnessContrast(img,brightness=0):
    
    # getTrackbarPos returns the current
    # position of the specified trackbar.
    brightness = cv2.getTrackbarPos('Brightness','Trackbar')
     
    contrast = cv2.getTrackbarPos('Contrast','Trackbar')
 
    effect = controller(img, brightness,
                        contrast)
 
    # The function imshow displays an image
    # in the specified window
    
    return effect

def controller(img, brightness=255,contrast=127):
   
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
 
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
 
    if brightness != 0:
 
        if brightness > 0:
 
            shadow = brightness
 
            max = 255
 
        else:
 
            shadow = 0
            max = 255 + brightness
 
        al_pha = (max - shadow) / 255
        ga_mma = shadow
 
        # The function addWeighted calculates
        # the weighted sum of two arrays
        cal = cv2.addWeighted(img, al_pha,
                              img, 0, ga_mma)
 
    else:
        cal = img
 
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
 
        # The function addWeighted calculates
        # the weighted sum of two arrays
        cal = cv2.addWeighted(cal, Alpha,
                              cal, 0, Gamma)
 
 
    return cal
 
def segmentation():
   
    if global_var.filepath == None:
        errorwindow("No Image Availble! (Please Browse file first)")
    else:
        image = cv2.imread(global_var.filepath)
        # convert to RGB
        image1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # reshape the image to a 2D array of pixels and 3 color values (RGB)
        pixel_values = image1.reshape((-1, 3))
        # convert to float
        pixel_values = np.float32(pixel_values)

        #print(pixel_values.shape)

        # define stopping criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

        # number of clusters (K)
        k = 7
        _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # convert back to 8 bit values
        centers = np.uint8(centers)

        # flatten the labels array
        labels = labels.flatten()

        # convert all pixels to the color of the centroids
        segmented = centers[labels.flatten()]

        # reshape back to the original image dimension
        segmented = segmented.reshape(image1.shape)

        segmented = cv2.cvtColor(segmented, cv2.COLOR_BGR2RGB)
       

        global_var.segmented_image = segmented
        global_var.Preview_flag = 1
        global_var.Stained_preset = 0

def adjustloop():

    if global_var.Stop_flag == 1:
        cv2.destroyAllWindows()
        global_var.Trackbar_flag = 0
    else:
        ##################################   RGB   Adjust   ##########################################   
        # convert to RGB
        rgb_edit = global_var.segmented_image.copy()
        rgb = cv2.cvtColor(rgb_edit, cv2.COLOR_BGR2RGB)
        r,g,b = cv2.split(rgb)


        r_pos = cv2.getTrackbarPos("R", "Trackbar")
        g_pos = cv2.getTrackbarPos("G", "Trackbar")
        b_pos = cv2.getTrackbarPos("B", "Trackbar")

        if r_pos >= 100 :
            rnew = (r + (((r_pos - 100) / 100)*(255-r))).astype(np.uint8)
        else:
            rnew = (r + (((r_pos - 100) / 100)*(r))).astype(np.uint8)

        if g_pos >= 100 :
            gnew = (g + (((g_pos - 100) / 100)*(255-g))).astype(np.uint8)
        else:
            gnew = (g + (((g_pos - 100) / 100)*(g))).astype(np.uint8)   

        if b_pos >= 100 :
            bnew = (b + (((b_pos - 100) / 100)*(255-b))).astype(np.uint8)
        else:
            bnew = (b + (((b_pos - 100) / 100)*(b))).astype(np.uint8)         

        # recombine channels
        rgb_new = cv2.merge([rnew,gnew,bnew])

        # convert back to bgr
        bgr_new = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)

        #########################################   Brightness & Contrast   ###############################################

        global_var.img = bgr_new.copy()

        global_var.img = BrightnessContrast(global_var.img,0)

        ######################################  Drawing Contour ############################################## 

        draw_contour = global_var.segmented_image.copy()

        thresh1 = cv2.getTrackbarPos("Threshold1", "Trackbar")
        thresh2 = cv2.getTrackbarPos("Threshold2", "Trackbar")
        boldness = cv2.getTrackbarPos("Boldness", "Trackbar")

        gray = cv2.cvtColor(draw_contour, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        edged = cv2.Canny(blurred, thresh1, thresh2, 3)
        dilated = cv2.dilate(edged, (1, 1), iterations=2)

        contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        Choose_Filter()

        cv2.drawContours(global_var.img, contours, -1, (0, 0, 0), boldness)
        # show the image

        resize = ResizeWithAspectRatio(global_var.img, width=500)
        cv2.imshow("Output", resize)

        k = cv2.waitKey(300) & 0xFF
        if k == 27 or global_var.Stop_flag == 1:
            global_var.Stop_flag = 1
            cv2.destroyAllWindows()
            global_var.Trackbar_flag = 0
        else:
            global_var.window.after(100, adjustloop)

