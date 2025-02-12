import cv2
from scipy.spatial import Voronoi
import numpy as np
import matplotlib.pyplot as plt
import os
import global_var
from utils import ResizeWithAspectRatio,errorwindow,Choose_Filter
import warnings

warnings.filterwarnings("ignore")

voronoi = None

# loop for showing stained glass-like pic
def GeometryLoop():

    k = cv2.waitKey(300) & 0xFF
    
    if k == 27 or global_var.Stop_flag == 1:
        global_var.Stop_flag = 1
        cv2.destroyAllWindows()
    else:
        resize = ResizeWithAspectRatio(global_var.geometric_image, width=500)
        cv2.imshow("Output", resize)
        global_var.window.after(100, GeometryLoop)

# segmentation based on voronoi area, resulting color in stained glass pic
def plot_voronoi(ax, img, x, y):

    global voronoi
    points = np.c_[x, y]
    voronoi = Voronoi(points)

    for region_idx, (x, y) in zip(voronoi.point_region, points):
        region = voronoi.regions[region_idx]
        # fill color based on voronoi region
        if not -1 in region:
            polygon = [voronoi.vertices[i] for i in region]
            color = "#{:02x}{:02x}{:02x}".format(*img[y, x, :])
            ax.fill(*zip(*polygon), color=color,lw=1, ec='k')

    ax.set_xlim((0, size_x))
    ax.set_ylim((0, size_y))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect(1)

# algorithm for generate stained glass-like image using voronoi plot as a line plot
def GeometrySegmentation():
      
    if global_var.filepath == None:
        errorwindow("No Image Availble! (Please Browse file first)")
    else:
        
        #Filter 
        global_var.img = cv2.imread(global_var.filepath)
        Choose_Filter()
        temp_filtered = os.path.join(os.path.dirname(__file__), 'temp/filtered.png')
        cv2.imwrite(temp_filtered, global_var.img)

        global_var.img = None


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

        global_var.geometric_image = newimage
        global_var.img = newimage
        global_var.Preview_flag = 1
        global_var.Stained_preset = 1