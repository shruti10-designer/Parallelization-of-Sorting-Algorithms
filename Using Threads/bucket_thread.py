import random
import time
import threading

def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key

def bucket_sort_parallel(arr):
    num_buckets = len(arr)
    buckets = [[] for _ in range(num_buckets)]
    max_val = max(arr)
    min_val = min(arr)
    bucket_range = (max_val - min_val) / num_buckets

    # Distribute elements into buckets
    for num in arr:
        index = int((num - min_val) // bucket_range)  # Calculate bucket index (fixed)
        if index >= num_buckets:  # Adjust index if it exceeds the range
            index = num_buckets - 1
        buckets[index].append(num)

    # Create threads for sorting buckets
    threads = []
    for bucket in buckets:
        thread = threading.Thread(target=insertion_sort, args=(bucket,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Concatenate sorted buckets into a single sorted array
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr

def generate_random_array(size):
    return [random.randint(0, 10000) for _ in range(size)]

def calculate_speedup(seq_time, parallel_time):
    return seq_time / parallel_time

def calculate_efficiency(speedup, num_threads):
    return speedup / num_threads

# Generate random array
array_size = 5000
array = generate_random_array(array_size)

# Sequential bucket sort
start_time = time.time()
sorted_array_seq = bucket_sort_parallel(array.copy())
seq_time = time.time() - start_time
print("Sequential Time:", seq_time)

# Parallel bucket sort
start_time = time.time()
sorted_array_parallel = bucket_sort_parallel(array)
parallel_time = time.time() - start_time
print("Parallel Time:", parallel_time)

# Calculate speedup and efficiency
speedup = calculate_speedup(seq_time, parallel_time)
efficiency = calculate_efficiency(speedup, 1)
print("Speedup:", speedup)
print("Efficiency:", efficiency)
