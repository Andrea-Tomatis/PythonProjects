'''
HowSum Problem

@Andrea-Tomatis

2022
'''

#recursive solution
def howSum(targetSum, numbers):
    if targetSum == 0:
        return []

    if targetSum < 0:
        return None
    
    for i in numbers:
        new_target = targetSum - i
        combination = howSum(new_target, numbers)
        if combination is not None:
            print(combination)
            return combination.append(new_target)
    
    return None


#iterative solution using tabulation
def howSum_tab(targetSum, numbers):
    arr = [[]]
    for _ in range(targetSum):
        arr.append(None)
    
    for i in range(targetSum+1):
        if arr[i] == None:
            continue
        
        current = arr[i]
        for n in numbers:
            try:
                if arr[i+n] is None:
                    arr[i + n] = [n]
                else: arr[i + n].append(n)
            except: pass
            
    return arr[targetSum]
    

def main():
    print(howSum(7, [3,4,7]))
    print(howSum_tab(7, [3,4,7]))
    #print(howSum(7, [2,3,4,5,6]))
    #print(isSum(1001, [2,4,6]))

if __name__ == '__main__':
    main()
