import matplotlib.pyplot as plt
import numpy as np
class Plot_2D(object):
        def __init__(self, x_arr, y_arr, dots = True, label = 'No Label'):
            self.data_x = x_arr
            self.data_y = y_arr
            self.dots = dots
            self.label = label

        def plotData(self):
            plt.figure(1)

            if self.dots:
                plt.scatter(self.data_x, self.data_y, marker= 'x', label=self.label)
            else:
                plt.plot(self.data_x, self.data_y, '-', label=self.label)

            plt.show()
