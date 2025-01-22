
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path
from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from scipy.spatial import Voronoi


# Linked to gui file path
#ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets/frame0')
#assert os.path.exists(ASSETS_PATH)

Light_Asset_Path = os.path.join(os.path.dirname(__file__), 'assets/Light_Asset')
assert os.path.exists(Light_Asset_Path)

Dark_Asset_Path = os.path.join(os.path.dirname(__file__), 'assets/Dark_Asset')
assert os.path.exists(Dark_Asset_Path)

ASSETS_PATH = Light_Asset_Path

Trackbar_flag = 0
filepath = None
Savepath = None
Stained_preset = 0
geometric_image = None
segmented_image = None
img = None
Save_flag = 0
Preview_flag = 1
Stop_flag = 0
filter_flag = 0
Asset_change = 0
voronoi = None
size_y, size_x, _ = None,None,None

##################################################################
def open():
    global filepath
    window.filename = filedialog.askopenfilename(initialdir="/image", title="Select a file",filetypes=(("jpg files", "*.jpg"),("png files", "*.png"),("all files", "*.*")))
    filepath = window.filename

   
def errorwindow(errortext):
    top= Toplevel(window)
    top.geometry("350x100")
    top.title("Error")
    Label(top, text= errortext, font=("Helvetica", 10)).pack(pady=20)
    B1 = Button(top, text="Okay", command = top.destroy)
    B1.pack()

def savesuccess():
    top= Toplevel(window)
    top.geometry("350x100")
    top.title("Success!")
    Label(top, text="Saving Success!", font=("Helvetica", 10)).pack(pady=20)
    B1 = Button(top, text="Okay", command = top.destroy)
    B1.pack()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def nothing(x):
    pass

def createTrackBar():

    global Trackbar_flag
    Trackbar_flag = 1

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

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def ChangeAsset():
    global Asset_change
    global ASSETS_PATH
    global Light_Asset_Path
    global Dark_Asset_Path

    if Asset_change == 0:
        ASSETS_PATH = Dark_Asset_Path
        Asset_change = 1
    else:
        ASSETS_PATH = Light_Asset_Path
        Asset_change = 0

def SaveImage():
        global img
        global Save_flag
        if Save_flag == 0:
            errorwindow("Could not save (No image Availble!)")
        else:
            img_save = img
            global Savepath
            window.filesave = filedialog.asksaveasfilename(initialdir="/assets",defaultextension='*.png', title="Select a folder",filetypes=(("jpg files", "*.jpg"),("png files", "*.png"),("all files", "*.*")))
            Savepath = window.filesave
            cv2.imwrite(Savepath, img_save)
            savesuccess()


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
 
def controller(img, brightness=255,
               contrast=127):
   
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
    
    global filepath
   
    if filepath == None:
        errorwindow("No Image Availble! (Please Browse file first)")
    else:
        image = cv2.imread(filepath)
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
       

        global segmented_image
        segmented_image = segmented
        global Preview_flag
        Preview_flag = 1
        global Stained_preset
        Stained_preset = 0

def adjustloop():

    global Stop_flag
    global Trackbar_flag
    if Stop_flag == 1:
        cv2.destroyAllWindows()
        Trackbar_flag = 0
    else:
        ##################################   RGB   Adjust   ##########################################   
        # convert to RGB
        rgb_edit = segmented_image.copy()
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
        global img
        img = bgr_new.copy()

        img = BrightnessContrast(img,0)

        ######################################  Drawing Contour ############################################## 

        draw_contour = segmented_image.copy()

        thresh1 = cv2.getTrackbarPos("Threshold1", "Trackbar")
        thresh2 = cv2.getTrackbarPos("Threshold2", "Trackbar")
        boldness = cv2.getTrackbarPos("Boldness", "Trackbar")

        gray = cv2.cvtColor(draw_contour, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        edged = cv2.Canny(blurred, thresh1, thresh2, 3)
        dilated = cv2.dilate(edged, (1, 1), iterations=2)

        contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        Choose_Filter()

        cv2.drawContours(img, contours, -1, (0, 0, 0), boldness)
        # show the image

        resize = ResizeWithAspectRatio(img, width=500)
        cv2.imshow("Output", resize)

        k = cv2.waitKey(300) & 0xFF
        if k == 27 or Stop_flag == 1:
            Stop_flag = 1
            cv2.destroyAllWindows()
            Trackbar_flag = 0
        else:
            window.after(100, adjustloop)

def ChangeFilterFlag(value):
    global filter_flag
    global Stop_flag
    global Stained_preset
    filter_flag = value
    if Stained_preset == 1:
        Stop_flag = 1 
        GeometrySegmentation()
        Showpic()

def StartPreviewloop():

        if Trackbar_flag == 0:
            createTrackBar()
        adjustloop()


def StopLoop():
    global Trackbar_flag
    global Stop_flag
    Trackbar_flag = 0
    Stop_flag = 1

def Showpic():
    global Stained_preset
    global Stop_flag
    if Preview_flag == 1:

        global Save_flag
        global Stop_flag

        Stop_flag = 0
        Save_flag = 1

        if Stained_preset == 1:
            GeometryLoop()
        else:
            StartPreviewloop()
    else:
        errorwindow("No Image Availble! (Please Browse file first)")
    
        
def GeometryLoop():

    global Stained_preset
    global Stop_flag

    k = cv2.waitKey(300) & 0xFF
    
    if k == 27 or Stop_flag == 1:
        Stop_flag = 1
        cv2.destroyAllWindows()
    else:
        resize = ResizeWithAspectRatio(geometric_image, width=500)
        cv2.imshow("Output", resize)
        window.after(100, GeometryLoop)




def plot_voronoi(ax, img, x, y):

    global voronoi
    points = np.c_[x, y]
    voronoi = Voronoi(points)

    for region_idx, (x, y) in zip(voronoi.point_region, points):
        region = voronoi.regions[region_idx]
        if not -1 in region:
            polygon = [voronoi.vertices[i] for i in region]
            color = "#{:02x}{:02x}{:02x}".format(*img[y, x, :])
            ax.fill(*zip(*polygon), color=color,lw=1, ec='k')

    ax.set_xlim((0, size_x))
    ax.set_ylim((0, size_y))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect(1)

def GeometrySegmentation():
    global filepath    
    if filepath == None:
        errorwindow("No Image Availble! (Please Browse file first)")
    else:
        global img
        #Filter 
        img = cv2.imread(filepath)
        Choose_Filter()
        temp_filtered = os.path.join(os.path.dirname(__file__), 'temp/filtered.png')
        cv2.imwrite(temp_filtered, img)

        img = None


        image = cv2.imread(temp_filtered)[::-1, :, ::-1]
        global size_y, size_x, _
        size_y, size_x, _ = image.shape
        
        fig = plt.figure(frameon=False)
        plt.imshow(image, origin="upper")
        nb_points = 1000
        ax = plt.axes()
        x = np.random.randint(0, size_x, nb_points)
        y = np.random.randint(0, size_y, nb_points)
        plot_voronoi(ax, image, x, y)


        k = np.ones((5, 5), np.float32) / 25
        edge_detection = cv2.filter2D(
            cv2.Laplacian(cv2.filter2D(image, -1, k), -1).max(axis=2), -1, k
        )


        sampling_prob = edge_detection.ravel() + .5
        idx = np.random.choice(
            sampling_prob.size,
            nb_points,
            replace=False,
            p=sampling_prob / sampling_prob.sum(),
        )
        x_edge, y_edge = idx % size_x, idx // size_x

        plt.imshow(image, origin="upper", alpha=.5)
        plot_voronoi(ax, image, x_edge, y_edge)
        plt.axis('off')
        temp_out = os.path.join(os.path.dirname(__file__), 'temp/out.png')
        fig.savefig(temp_out, bbox_inches='tight', pad_inches=0)

        newimage = cv2.imread(temp_out)
        global geometric_image
        geometric_image = newimage
        img = newimage
        global Preview_flag
        Preview_flag = 1
        global Stained_preset
        Stained_preset = 1



def Choose_Filter():
    global filter_flag
    global img

    if filter_flag == 0 :
        pass
    elif filter_flag == 1:
        img = cv2.applyColorMap(img, cv2.COLORMAP_SUMMER)
    elif filter_flag == 2:
        img = cv2.applyColorMap(img, cv2.COLORMAP_SPRING)
    elif filter_flag == 3:
        img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
    elif filter_flag == 4:
        img = cv2.applyColorMap(img, cv2.COLORMAP_WINTER)
    elif filter_flag == 5:
        img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
    elif filter_flag == 6:
        img = cv2.applyColorMap(img, cv2.COLORMAP_COOL)
    elif filter_flag == 7:
        img = cv2.applyColorMap(img, cv2.COLORMAP_PARULA)
    elif filter_flag == 8:
        img = cv2.applyColorMap(img, cv2.COLORMAP_MAGMA)
    elif filter_flag == 9:
        img = cv2.applyColorMap(img, cv2.COLORMAP_VIRIDIS)
    elif filter_flag == 10:
        img = cv2.applyColorMap(img, cv2.COLORMAP_TWILIGHT)
    elif filter_flag == 11:
        img = cv2.applyColorMap(img, cv2.COLORMAP_TURBO)




        

#######################################################################

window = Tk()
window.title('Stainomic')
window.geometry("1024x720")
window.configure(bg = "#FFFFFF")

#######################################################################


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    512.0,
    360.0,
    image=image_image_1
)

canvas.create_text(
    618.0,
    398.0,
    anchor="nw",
    text="Filter",
    fill="#FFFFFF",
    font=("Inter Medium", 36 * -1)
)

canvas.create_text(
    523.0,
    87.0,
    anchor="nw",
    text="Stainomic",
    fill="#521E58",
    font=("Inter SemiBold", 64 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open,
    relief="flat"
)
button_1.place(
    x=415.0,
    y=206.0,
    width=270.0,
    height=64.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=GeometrySegmentation,
    relief="flat"
)
button_2.place(
    x=415.0,
    y=281.0,
    width=270.0,
    height=68.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=SaveImage,
    relief="flat"
)
button_3.place(
    x=707.0,
    y=204.0,
    width=270.0,
    height=68.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=Showpic,
    relief="flat"
)
button_4.place(
    x=415.0,
    y=652.0,
    width=270.0,
    height=64.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=StopLoop,
    relief="flat"
)
button_5.place(
    x=707.0,
    y=650.0,
    width=270.0,
    height=68.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(1),
    relief="flat"
)
button_6.place(
    x=424.0,
    y=474.0,
    width=68.0,
    height=69.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(2),
    relief="flat"
)
button_7.place(
    x=518.0,
    y=474.0,
    width=68.0,
    height=69.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(3),
    relief="flat"
)
button_8.place(
    x=610.0,
    y=474.0,
    width=68.0,
    height=69.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(4),
    relief="flat"
)
button_9.place(
    x=701.0,
    y=474.0,
    width=68.0,
    height=69.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(5),
    relief="flat"
)
button_10.place(
    x=793.0,
    y=475.0,
    width=68.0,
    height=69.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(6),
    relief="flat"
)
button_11.place(
    x=884.0,
    y=474.0,
    width=68.0,
    height=69.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(7),
    relief="flat"
)
button_12.place(
    x=475.0,
    y=559.0,
    width=68.0,
    height=69.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(8),
    relief="flat"
)
button_13.place(
    x=569.0,
    y=559.0,
    width=68.0,
    height=69.0
)

button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(9),
    relief="flat"
)
button_14.place(
    x=661.0,
    y=559.0,
    width=68.0,
    height=69.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(10),
    relief="flat"
)
button_15.place(
    x=751.0,
    y=559.0,
    width=68.0,
    height=69.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(11),
    relief="flat"
)
button_16.place(
    x=844.0,
    y=559.0,
    width=68.0,
    height=69.0
)

button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ChangeFilterFlag(0),
    relief="flat"
)
button_17.place(
    x=935.0,
    y=559.0,
    width=68.0,
    height=69.0
)

button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=segmentation,
    relief="flat"
)
button_18.place(
    x=707.0,
    y=281.0,
    width=270.0,
    height=68.0
)


window.resizable(False, False)

##############################################################################

if filepath is None:
    Preview_flag = 0
else:
    Preview_flag = 1


##############################################################################

window.mainloop()
