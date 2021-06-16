'''
Implement a simple Galton Board (also knows as Quincunx) in python

@Andrea Tomatis
'''

import random
import time
import matplotlib.pyplot as plt

def main():
    matrix = [[0 for i in range(101)] for i in range(51)]

    with open('test.csv','a') as fp:
        for i in range(100):
            for _ in range(10000):
                x = len(matrix[0])//2
                y = 0
                for i in range(len(matrix)-1):
                    #edit the row below to change the probability that the ball will fall to the right or left
                    x += random.choice([1,-1])
                    y += 1
                matrix[y][x] += 1
            fp.write(','.join(str(matrix[-1][i]) for i in range(0,len(matrix[-1]),2)) + '\n')
        
        #with this you won't plot the empty column (odd)
        plot = []
        for i in range(len(matrix[-1])):
            if i % 2 == 0: plot.append(matrix[-1][i])
        plt.bar([i for i in range(len(plot))],plot)
        plt.show()


if __name__ == '__main__':
    main()
