'''
L'ago di Buffon
Simulazione con matplotlib per l'approssimazione del pi greco
'''

import math
import random
import matplotlib.pyplot as plt
import decimal as dc

L = 2
D = 20
MATRIX_WIDTH = D*5 + 30
MATRIX_HEIGHT = D*2 + 30
N_TRIALS = 1000
PRECISION = 20

dc.getcontext().prec = PRECISION
plt.style.use('ggplot')

def find_next(x):
    i = x // D
    j = D * i
    return j + D
    
    
def main():
    trials_cnt = 0
    win_cnt = 0
    fig, ax1 = plt.subplots(1, 1)
    
    
    while trials_cnt < N_TRIALS:
        center_x = random.uniform(0, MATRIX_WIDTH)
        center_y = random.uniform(0, MATRIX_HEIGHT)
        
        alpha = random.randint(90,270)
        c = L/2 * math.cos(math.radians(alpha))
        b = L/2 * math.sin(math.radians(alpha))
        a_x = center_x + c
        a_y = center_y + b
        
        b_x = center_x - c
        b_y = center_y - b
        
        next_d = find_next(a_x)
        
        if next_d <= b_x or a_x % D == 0:
            win_cnt += 1
            ax1.plot([a_x, b_x], [a_y, b_y], color='g')
            ax1.plot([center_x],[center_y], 'go')
        else:
            ax1.plot([a_x, b_x], [a_y, b_y], color='r', alpha=.2)
    
        trials_cnt += 1
        
    
    pi_approximation = dc.Decimal(2 * L * trials_cnt) / dc.Decimal(D * win_cnt)

    print(f'The approximated value of pi is: {pi_approximation}')
    
    for i in range(0, MATRIX_WIDTH, D):
        ax1.plot([i for j in range (MATRIX_HEIGHT)],
                 [j for j in range(MATRIX_HEIGHT)],
                 color='y')
    
    plt.xlim(right=MATRIX_WIDTH)
    plt.ylim(top=MATRIX_HEIGHT)
    plt.show()


if __name__ == '__main__':
    main()
