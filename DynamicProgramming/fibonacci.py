'''
Fibonacci Problem

@Andrea-Tomatis

2022
'''

#recursive solution using memoization
def fib(n, memo={}):
    if n <=2:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]


#iterative solution using tabulation
def fib_tab(n):
    arr = [0,1]
    for i in range(n):
        arr.append(0)
    
    for i in range(n):
        current = arr[i]
        arr[i+1] += current
        arr[i+2] += current
        
    return arr[n]


if __name__ == '__main__':
    print(fib_tab(6))
