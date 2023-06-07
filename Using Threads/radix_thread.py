import random
import time
import threading

def radix_sort_parallel(arr, num_threads):
    max_value = max(arr)
    exp = 1

    while max_value // exp > 0:
        buckets = [[] for _ in range(10)]  # Create 10 buckets for each digit

        # Divide the input into equal-sized chunks
        chunk_size = len(arr) // num_threads
        chunks = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]

        threads = []

        # Create threads for distributing elements into buckets
        for chunk in chunks:
            thread = threading.Thread(target=distribute_to_buckets, args=(chunk, buckets, exp))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Merge the buckets into a single sorted array
        arr = []
        for bucket in buckets:
            arr.extend(bucket)

        exp *= 10  # Move to the next significant digit

    return arr

def distribute_to_buckets(arr, buckets, exp):
    for num in arr:
        index = (num // exp) % 10
        buckets[index].append(num)

def generate_random_array(size):
    return [random.randint(0, 10000) for _ in range(size)]

def calculate_speedup(seq_time, parallel_time):
    return seq_time / parallel_time

def calculate_efficiency(speedup, num_threads):
    return speedup / num_threads

# Generate random array
array_size = 5000
array = generate_random_array(array_size)

# Sequential radix sort
start_time = time.time()
sorted_array_seq = sorted(array)
seq_time = time.time() - start_time
print("Sequential Time:", seq_time)

# Parallel radix sort with 4 threads
start_time = time.time()
sorted_array_parallel = radix_sort_parallel(array, 4)
parallel_time = time.time() - start_time
print("Parallel Time:", parallel_time)

# Calculate speedup and efficiency
speedup = calculate_speedup(seq_time, parallel_time)
efficiency = calculate_efficiency(speedup, 4)
print("Speedup:", speedup)
print("Efficiency:", efficiency)
