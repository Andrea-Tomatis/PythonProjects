'''
Grid Travel Problem

@Andrea-Tomatis

2022
'''

#recursive solution using memoization
def gridTravel(m, n, memo={}):
    key = str(m) + ',' + str(n)
    if m == 1 and n == 1:
        return 1
    if not m or not n:
        return 0
    if key in memo:
        return memo[key]
    memo[key] = gridTravel(m-1, n, memo) + gridTravel(m, n-1, memo)
    return memo[key]
    

#iterative solution using tabulation
def gridTravel_tab(m, n):
    arr = []
    for _ in range(m+1):
        row =  []
        for _ in range(n+1):
            row.append(0)
        arr.append(row)
    arr[1][1] = 1
    
    for i in range(m+1):
        for j in range(n+1):
            current = arr[i][j]
            try: arr[i+1][j] += current
            except: pass
            
            try: arr[i][j+1] += current
            except: pass
            
    return arr[m][n]


def main():
    print(gridTravel(2,3))
    print(gridTravel_tab(2,3))
    #print(gridTravel(2,3))
    #print(gridTravel(0,8))
    #print(gridTravel(18,18))

if __name__ == '__main__':
    main()
