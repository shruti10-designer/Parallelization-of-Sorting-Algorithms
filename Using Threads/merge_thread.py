import random
import time
import threading

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged

def merge_sort_parallel(arr):
    if len(arr) <= 1:
        return arr
    threads = []
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # Create threads
    left_thread = threading.Thread(target=merge_sort_parallel, args=(left,))
    right_thread = threading.Thread(target=merge_sort_parallel, args=(right,))
    threads.append(left_thread)
    threads.append(right_thread)
    
    # Start threads
    left_thread.start()
    right_thread.start()

    # Wait for threads to complete
    left_thread.join()
    right_thread.join()

    return merge(left, right)

def generate_random_array(size):
    return [random.randint(0, 10000) for _ in range(size)]

def calculate_speedup(seq_time, parallel_time):
    return seq_time / parallel_time

def calculate_efficiency(speedup, num_threads):
    return speedup / num_threads

# Generate random array
array_size = 5000
array = generate_random_array(array_size)

# Sequential mergesort
start_time = time.time()
sorted_array_seq = merge_sort(array.copy())
seq_time = time.time() - start_time
print("Sequential Time:", seq_time)

# Parallel mergesort
start_time = time.time()
sorted_array_parallel = merge_sort_parallel(array)
parallel_time = time.time() - start_time
print("Parallel Time:", parallel_time)

# Calculate speedup and efficiency
speedup = calculate_speedup(seq_time, parallel_time)
efficiency = calculate_efficiency(speedup, 2)
print("Speedup:", speedup)
print("Efficiency:", efficiency)
