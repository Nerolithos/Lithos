import random
import time

random_numbers = [random.randint(1000,9999) for _ in range(1000)]
print(random_numbers)
print("\n\n")




# 冒泡排序法
def bubble(arrange):
    cn = 0
    length = len(arrange)
    for compared_elements in range(length):
        for num in range(0, length - compared_elements - 1):
            if arrange[num] > arrange[num + 1]:
                arrange[num], arrange[num + 1] = arrange[num + 1], arrange[num]
                cn += 1
    return arrange, cn

start_time = time.time()
sorted_numbers, cn = bubble(random_numbers)
end_time = time.time()
elapsed_time1 = end_time - start_time

# print(sorted_numbers)
print("\n\n")




# 快排序
comparison_count = 0

def quick_sort(arr):
    global comparison_count
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    comparison_count += len(arr)  # 更新比较次数
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    comparison_count += len(arr)  # 更新比较次数
    
    return quick_sort(left) + middle + quick_sort(right)

start_time = time.time()
sorted_numbers = quick_sort(random_numbers)
end_time = time.time()
elapsed_time2 = end_time - start_time

# print(sorted_numbers)
print("\n\n")




print(f"bubble, times: {cn}, duration: {elapsed_time1:.6f}.")
print(f"quick, times: {comparison_count}, duration: {elapsed_time2:.6f}.")





