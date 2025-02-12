from tkinter import *


img = None
filepath = None
Savepath = None
Save_flag = 0
Trackbar_flag = 0
Stained_preset = 0
geometric_image = None
segmented_image = None
Preview_flag = 1
Stop_flag = 0
Asset_change = 0
size_y, size_x, _ = None,None,None



window = Tk()
window.title('Stainomic')
window.geometry("1024x720")
window.configure(bg = "#FFFFFF")
window.resizable(False, False)


if filepath is None:
    Preview_flag = 0
else:
    Preview_flag = 1