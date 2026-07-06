import random
n = 10000

l = []
for i in range(n):
    l.append(round(random.uniform(5,9999)))

def quickshort(arr):
    _quickshort(arr, 0, len(arr)-1)

def _quickshort(arr, low, high):
    if low < high:
        pivot = parttion(arr, low, high)
        _quickshort(arr, low, pivot-1)
        _quickshort(arr, pivot+1, high)

def parttion(arr, low, high):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] <= pivot:
            arr[j], arr[i] = arr[i], arr[j]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i
    
quickshort(l)
print(l)
        