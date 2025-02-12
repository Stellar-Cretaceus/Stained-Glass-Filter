import os
from pathlib import Path
from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Canvas,Button, PhotoImage
import global_var,comicFunc,stainedFunc,utils

# Linked to gui file path
#ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets/frame0')
#assert os.path.exists(ASSETS_PATH)

Light_Asset_Path = os.path.join(os.path.dirname(__file__), 'assets/Light_Asset')
assert os.path.exists(Light_Asset_Path)

Dark_Asset_Path = os.path.join(os.path.dirname(__file__), 'assets/Dark_Asset')
assert os.path.exists(Dark_Asset_Path)

ASSETS_PATH = Light_Asset_Path



##################################################################
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def ChangeFilterFlag(value):
    utils.filter_flag = value
    if global_var.Stained_preset == 1:
        global_var.Stop_flag = 1 
        stainedFunc.GeometrySegmentation()
        Showpic()

def StartPreviewloop():

        if global_var.Trackbar_flag == 0:
           comicFunc.createTrackBar()
        comicFunc.adjustloop()


def StopLoop():
    global_var.Trackbar_flag = 0
    global_var.Stop_flag = 1

def Showpic():

    if global_var.Preview_flag == 1:
        global_var.Stop_flag = 0
        global_var.Save_flag = 1

        if global_var.Stained_preset == 1:
            stainedFunc.GeometryLoop()
        else:
            StartPreviewloop()
    else:
        utils.errorwindow("No Image Availble! (Please Browse file first)")
    

#######################################################################


canvas = Canvas(
    global_var.window,
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
    command=utils.open,
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
    command=stainedFunc.GeometrySegmentation,
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
    command=utils.SaveImage,
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
    command=comicFunc.segmentation,
    relief="flat"
)
button_18.place(
    x=707.0,
    y=281.0,
    width=270.0,
    height=68.0
)

##############################################################################

global_var.window.mainloop()
