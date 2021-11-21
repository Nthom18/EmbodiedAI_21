'''
Plotting csv files for

Author: Nicoline Louise Thomsen
'''

import csv
import matplotlib.pyplot as plt

t = []
cl1 = []
cl2 = []


def plotCSV_d(filename):
    
    with open('Logs/' + filename + '.csv','r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        next(plots) # Skip header
        for row in plots:
            t.append(int(row[0]))
            cl1.append(float(row[1]))
            cl2.append(float(row[2]))
            

    plt.plot(t, cl1, label = 'cl1')
    plt.plot(t, cl2, label = 'cl2')
    
    plt.xlabel('Time steps')
    plt.ylabel('Light intensity')
    plt.title('Distance to target')
    plt.legend()
    
    plt.show()
    


if __name__ == '__main__':
    plotCSV_d('data_205826')
