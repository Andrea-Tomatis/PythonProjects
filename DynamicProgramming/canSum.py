'''
CanSum Problem

@Andrea-Tomatis

2022
'''

#recursive solution using memoization
def canSum(targetSum, numbers, memo={}):
    if targetSum == 0:
        return True

    if targetSum in memo:
        return memo[targetSum]

    if targetSum < 0:
        return False
    
    for i in numbers:
        new_target = targetSum - i
        if canSum(new_target, numbers):
            memo[targetSum] = True
            return True
    
    memo[targetSum] = False
    return False


#iterative solution using tabulation
def canSum_tab(targetSum, numbers):
    arr = [True]
    for _ in range(targetSum):
        arr.append(False)
    
    for i in range(targetSum+1):
        if arr[i] == False:
            continue
        
        current = arr[i]
        for n in numbers:
            try: arr[i + n] = True
            except: pass
            
    return arr[targetSum]
        
    


def main():
    print(canSum(7, [2,3,4,5,6]))
    print(canSum_tab(7, [2,3,4,5,6]))
    print(canSum(7, [2,3,4,5,6]))
    print(canSum_tab(1001, [2,4,6]))

if __name__ == '__main__':
    main()
