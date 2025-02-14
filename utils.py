from tkinter import *
from tkinter import filedialog
import cv2
import global_var

# flag for filter applying
filter_flag = 0

# Save image popup using cv2
def SaveImage():
    if global_var.Save_flag == 0:
        errorwindow("Could not save (No image Availble!)")
    else:
        img_save = global_var.img
        global_var.filesave = filedialog.asksaveasfilename(initialdir="/assets",defaultextension='*.png', title="Select a folder",filetypes=(("jpg files", "*.jpg"),("png files", "*.png"),("all files", "*.*")))
        global_var.Savepath = global_var.filesave
        cv2.imwrite(global_var.Savepath, img_save)
        savesuccess()

# open image pop-up
def open():
    global filepath
    global_var.filename = filedialog.askopenfilename(initialdir="/image", title="Select a file",filetypes=(("jpg files", "*.jpg"),("png files", "*.png"),("all files", "*.*")))
    global_var.filepath = global_var.filename

# stop showpic
def StopLoop():
    global_var.Trackbar_flag = 0
    global_var.Stop_flag = 1

# universal error window
def errorwindow(errortext):
    top = Toplevel(global_var.window)
    top.geometry("350x100")
    top.title("Error")
    Label(top, text= errortext, font=("Helvetica", 10)).pack(pady=20)
    B1 = Button(top, text="Okay", command = top.destroy)
    B1.pack()

# success pop-up
def savesuccess():
    top= Toplevel(global_var.window)
    top.geometry("350x100")
    top.title("Success!")
    Label(top, text="Saving Success!", font=("Helvetica", 10)).pack(pady=20)
    B1 = Button(top, text="Okay", command = top.destroy)
    B1.pack()

# Resize Img func to fit pop-up
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

# literally nothing
def nothing(x):
    pass

# apply filter based on flag
def Choose_Filter():
    if filter_flag == 0 :
        pass
    elif filter_flag == 1:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_SUMMER)
    elif filter_flag == 2:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_SPRING)
    elif filter_flag == 3:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_AUTUMN)
    elif filter_flag == 4:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_WINTER)
    elif filter_flag == 5:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_HOT)
    elif filter_flag == 6:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_COOL)
    elif filter_flag == 7:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_PARULA)
    elif filter_flag == 8:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_MAGMA)
    elif filter_flag == 9:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_VIRIDIS)
    elif filter_flag == 10:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_TWILIGHT)
    elif filter_flag == 11:
        global_var.img = cv2.applyColorMap(global_var.img, cv2.COLORMAP_TURBO)



