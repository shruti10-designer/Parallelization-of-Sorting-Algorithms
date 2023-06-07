import random
import time
import threading

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def selection_sort_parallel(arr):
    threads = []
    num_threads = 4  # Number of threads to use
    chunk_size = len(arr) // num_threads

    # Create threads
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size
        thread = threading.Thread(target=selection_sort, args=(arr[start:end],))
        threads.append(thread)
        thread.start()

    # Wait for threads to complete
    for thread in threads:
        thread.join()

    # Merge the sorted chunks
    merge_chunks(arr, chunk_size)

def merge_chunks(arr, chunk_size):
    n = len(arr)
    for i in range(0, n-chunk_size, chunk_size):
        mid = i + chunk_size - 1
        end = min(i + 2*chunk_size - 1, n-1)
        merge(arr, i, mid, end)

def merge(arr, start, mid, end):
    left = arr[start:mid+1]
    right = arr[mid+1:end+1]
    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

def generate_random_array(size):
    return [random.randint(0, 10000) for _ in range(size)]

def calculate_speedup(seq_time, parallel_time):
    return seq_time / parallel_time

def calculate_efficiency(speedup, num_threads):
    return speedup / num_threads

# Generate random array
array_size = 5000
array = generate_random_array(array_size)

# Sequential selection sort
start_time = time.time()
selection_sort(array.copy())
seq_time = time.time() - start_time
print("Sequential Time:", seq_time)

# Parallel selection sort
start_time = time.time()
selection_sort_parallel(array)
parallel_time = time.time() - start_time
print("Parallel Time:", parallel_time)

# Calculate speedup and efficiency
speedup = calculate_speedup(seq_time, parallel_time)
efficiency = calculate_efficiency(speedup, 4)
print("Speedup:", speedup)
print("Efficiency:", efficiency)
