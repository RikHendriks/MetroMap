import numpy as np

import matplotlib.pyplot as plt
import svgpathtools as svg


class Canvas:
    def __init__(self):
        self.lines = []
        self.texts = []

    def draw_line(self, start, end, color='black'):
        self.lines.append([np.array([start, end]), color])

    def draw_text(self, coordinate, text, font_size=12, color='black'):
        self.texts.append([coordinate, text, font_size, color])

    def show_matplotlib(self, filename=None, plot_window=None, show_plot=False):
        # Plot each line to matplotlib
        for line in self.lines:
            plt.plot([line[0][0][0], line[0][1][0]], [line[0][0][1], line[0][1][1]], line[1])
        # Plot each text to matplotlib
        for text in self.texts:
            plt.text(text[0][0], text[0][1], text[1], fontsize=text[2], color=text[3])
        # Redefine the axis of the plot
        plt.axis(plot_window)
        # Save the plotted file
        if filename is not None:
            plt.savefig(filename)
        # Show the plot
        if show_plot:
            plt.show()

    def save_svg(self, filename):
        lines = [svg.Line(start[0] + start[1] * 1j, end[0] + end[1] * 1j) for start, end in self.lines]
        svg.wsvg(lines, filename=filename)