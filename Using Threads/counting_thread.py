import random
import time
import threading

def counting_sort_parallel(arr, num_threads):
    min_val = min(arr)
    max_val = max(arr)
    range_val = max_val - min_val + 1
    counts = [0] * range_val
    sorted_arr = [0] * len(arr)

    # Divide the input into equal-sized chunks
    chunk_size = (len(arr) + num_threads - 1) // num_threads
    chunks = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]

    # Create threads for counting
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=counting_thread, args=(counts, chunks[i], min_val))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Perform cumulative sum on counts array
    for i in range(1, len(counts)):
        counts[i] += counts[i-1]

    # Create threads for sorting
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=sorting_thread, args=(chunks[i], sorted_arr, counts, min_val))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return sorted_arr

def counting_thread(counts, arr, min_val):
    for num in arr:
        index = num - min_val
        counts[index] += 1

def sorting_thread(arr, sorted_arr, counts, min_val):
    for num in arr:
        index = num - min_val
        sorted_index = counts[index] - 1
        sorted_arr[sorted_index] = num
        counts[index] -= 1

def generate_random_array(size):
    return [random.randint(0, 10000) for _ in range(size)]

def calculate_speedup(seq_time, parallel_time):
    return seq_time / parallel_time

def calculate_efficiency(speedup, num_threads):
    return speedup / num_threads

# Generate random array
array_size = 5000
array = generate_random_array(array_size)

# Sequential counting sort
start_time = time.time()
sorted_array_seq = counting_sort_parallel(array.copy(), 1)
seq_time = time.time() - start_time
print("Sequential Time:", seq_time)

# Parallel counting sort with 4 threads
start_time = time.time()
sorted_array_parallel = counting_sort_parallel(array, 4)
parallel_time = time.time() - start_time
print("Parallel Time:", parallel_time)

# Calculate speedup and efficiency
speedup = calculate_speedup(seq_time, parallel_time)
efficiency = calculate_efficiency(speedup, 4)
print("Speedup:", speedup)
print("Efficiency:", efficiency)
