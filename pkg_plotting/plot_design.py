import math

import matplotlib.pyplot as plt
from pkg_plotting import window_design as wd
from pkg_elastic.utility import num_of_logs_for_sql_injection as num_logs
import random


def get_key_from_coord(x, y):
    return x + y + (x * 10)


def change_subplot(coord):
    if coord[1] >= 2:
        coord[0] = coord[0] + 1
        coord[1] = 0
    else:
        coord[1] = coord[1] + 1


def draw_lines(x, y, c_plt):
    c_plt.plot(x, y, '-')
    c_plt.axis('equal')


class ClusterPlot:
    def __init__(self, list_of_dict, graph_size):
        self.list_of_dict = list_of_dict
        self.graph_size = graph_size
        self.x = {}
        self.y = {}
        self.c = []
        self.clusters = {}
        self.clusters_type = {}
        self.sc = {}
        self.annot = {}

        _fig, _ax = plt.subplots(2, 3)
        self.fig = _fig
        self.ax = _ax
        self.names = ["Methods", "Requests", "Response Class", "Response Code", "Data Transfered", "Query"]
        self.set_points()

        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())

    def set_annotate(self, x, y):
        key = get_key_from_coord(x, y)
        self.annot[key] = self.ax[x, y].annotate("sa", xy=(0, 0), xytext=(1, 1), textcoords="offset points",
                                                 bbox=dict(boxstyle="round", fc="w"),
                                                 arrowprops=dict(arrowstyle="->"))
        self.annot[key].set_visible(False)

    def set_points(self):
        coord = [0, 0]
        names_index = 0
        for dictionar in self.list_of_dict:

            index = 0
            key = get_key_from_coord(coord[0], coord[1])
            self.x[key] = []
            self.y[key] = []
            self.c = []
            self.clusters[key] = {}
            self.clusters_type[key] = {}
            points_number = len(dictionar)
            for cluster_list in dictionar:
                color = random.uniform(1, 10)

                x_for_drawing_lines = []
                y_for_drawing_lines = []
                for cluster_num in cluster_list:
                    x_c = random.uniform(index, index + self.graph_size // points_number)
                    y_c = len(cluster_list[cluster_num])
                    self.x[key].extend([x_c])
                    self.y[key].extend([y_c])
                    self.c.extend([color])
                    self.clusters[key][x_c] = cluster_list[cluster_num]
                    self.clusters_type[key][x_c] = cluster_num
                    x_for_drawing_lines.append(x_c)
                    y_for_drawing_lines.append(y_c)

                draw_lines(x_for_drawing_lines, y_for_drawing_lines, self.ax[coord[0], coord[1]])
                # draw_lines(self.x[key], self.y[key], self.ax[coord[0], coord[1]])
                index = index + self.graph_size // points_number
            _sc = self.ax[coord[0], coord[1]].scatter(self.x[key], self.y[key], c=self.c, s=10, picker=True)
            self.ax[coord[0], coord[1]].set_xlim(0, self.graph_size)
            self.ax[coord[0], coord[1]].set_ylim(0, self.graph_size)
            self.ax[coord[0], coord[1]].title.set_text(self.names[names_index])
            names_index = names_index + 1
            self.sc[key] = _sc
            self.set_annotate(coord[0], coord[1])

            change_subplot(coord)

    def onclick(self, event):
        x_coord = event.xdata
        if event.inaxes == self.ax[0, 0]:
            key = get_key_from_coord(0, 0)
            cont, ind = self.sc[key].contains(event)
            self.show_window(cont, x_coord, key)
        elif event.inaxes == self.ax[0, 1]:
            key = get_key_from_coord(0, 1)
            cont, ind = self.sc[key].contains(event)
            self.show_window(cont, x_coord, key)
        elif event.inaxes == self.ax[0, 2]:
            key = get_key_from_coord(0, 2)
            cont, ind = self.sc[key].contains(event)
            self.show_window(cont, x_coord, key)
        elif event.inaxes == self.ax[1, 0]:
            key = get_key_from_coord(1, 0)
            cont, ind = self.sc[key].contains(event)
            self.show_window(cont, x_coord, key)
        elif event.inaxes == self.ax[1, 1]:
            key = get_key_from_coord(1, 1)
            cont, ind = self.sc[key].contains(event)
            self.show_window(cont, x_coord, key)
        elif event.inaxes == self.ax[1, 2]:
            key = get_key_from_coord(1, 2)
            cont, ind = self.sc[key].contains(event)
            self.show_window(cont, x_coord, key)

    def show_window(self, cont, x_coord, key):
        if cont:
            self.fig.canvas.draw_idle()
            list_of_clusters = list(self.clusters[key].keys())
            cluster_num = min_dif(list_of_clusters, x_coord)
            wd.show((self.clusters[key])[cluster_num], (self.clusters_type[key])[cluster_num])

    def make_plot(self):
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        plt.show()

    def update_annot(self, ind, y_coord, x, y):
        key = get_key_from_coord(x, y)
        pos = self.sc[key].get_offsets()[ind["ind"][0]]
        self.annot[key].xy = pos
        text = str(math.ceil(y_coord))
        self.annot[key].set_text(text)
        self.annot[key].get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        y_coord = event.ydata
        if event.inaxes == self.ax[0, 0]:
            self.show_log_quantity(event, 0, 0, y_coord)
        elif event.inaxes == self.ax[0, 1]:
            self.show_log_quantity(event, 0, 1, y_coord)
        elif event.inaxes == self.ax[0, 2]:
            self.show_log_quantity(event, 0, 2, y_coord)
        elif event.inaxes == self.ax[1, 0]:
            self.show_log_quantity(event, 1, 0, y_coord)
        elif event.inaxes == self.ax[1, 1]:
            self.show_log_quantity(event, 1, 1, y_coord)
        elif event.inaxes == self.ax[1, 2]:
            self.show_log_quantity(event, 1, 2, y_coord)

    def show_log_quantity(self, event, x, y, y_coord):
        key = get_key_from_coord(x, y)
        vis = self.annot[key].get_visible()
        cont, ind = self.sc[key].contains(event)
        if cont:
            self.update_annot(ind, y_coord, x, y)
            self.annot[key].set_visible(True)
            self.fig.canvas.draw_idle()
        else:
            if vis:
                self.annot[key].set_visible(False)
                self.fig.canvas.draw_idle()


def min_dif(list_of_val, val_to_compare):
    if len(list_of_val) <= 0:
        return 0
    minim = abs(val_to_compare - list_of_val[0])
    min_value = list_of_val[0]
    for val in list_of_val:
        if minim > abs((val_to_compare - val)):
            minim = abs(val_to_compare - val)
            min_value = val

    return min_value
