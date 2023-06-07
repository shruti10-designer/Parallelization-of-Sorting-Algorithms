import random
import time
import threading

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def insertion_sort_parallel(arr, num_threads):
    chunk_size = len(arr) // num_threads
    threads = []

    # Divide the input into equal-sized chunks
    chunks = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]

    # Create threads for sorting each chunk
    for chunk in chunks:
        thread = threading.Thread(target=insertion_sort, args=(chunk,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Merge the sorted chunks
    sorted_arr = merge_sorted_chunks(chunks)

    return sorted_arr

def merge_sorted_chunks(chunks):
    result = []
    while len(chunks) > 1:
        merged_chunk = merge_two_chunks(chunks.pop(0), chunks.pop(0))
        chunks.append(merged_chunk)
    if chunks:
        result = chunks[0]
    return result

def merge_two_chunks(chunk1, chunk2):
    merged = []
    i, j = 0, 0
    while i < len(chunk1) and j < len(chunk2):
        if chunk1[i] <= chunk2[j]:
            merged.append(chunk1[i])
            i += 1
        else:
            merged.append(chunk2[j])
            j += 1
    merged.extend(chunk1[i:])
    merged.extend(chunk2[j:])
    return merged

def generate_random_array(size):
    return [random.randint(0, 10000) for _ in range(size)]

def calculate_speedup(seq_time, parallel_time):
    return seq_time / parallel_time

def calculate_efficiency(speedup, num_threads):
    return speedup / num_threads

# Generate random array
array_size = 5000
array = generate_random_array(array_size)

# Sequential insertion sort
start_time = time.time()
sorted_array_seq = array.copy()
insertion_sort(sorted_array_seq)
seq_time = time.time() - start_time
print("Sequential Time:", seq_time)

# Parallel insertion sort with 4 threads
start_time = time.time()
sorted_array_parallel = insertion_sort_parallel(array, 4)
parallel_time = time.time() - start_time
print("Parallel Time:", parallel_time)

# Calculate speedup and efficiency
speedup = calculate_speedup(seq_time, parallel_time)
efficiency = calculate_efficiency(speedup, 4)
print("Speedup:", speedup)
print("Efficiency:", efficiency)
