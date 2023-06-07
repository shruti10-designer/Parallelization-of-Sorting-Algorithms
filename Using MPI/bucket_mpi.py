from mpi4py import MPI
import time

def bucket_sort_parallel(arr):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Split the array into equal parts
    local_size = len(arr) // size
    local_arr = arr[rank * local_size: (rank + 1) * local_size]

    # Determine the range of values in the local array
    local_min_val = min(local_arr) if len(local_arr) > 0 else float('inf')
    local_max_val = max(local_arr) if len(local_arr) > 0 else float('-inf')
    global_min_val = comm.allreduce(local_min_val, op=MPI.MIN)
    global_max_val = comm.allreduce(local_max_val, op=MPI.MAX)

    # Calculate the number of buckets and the range for each bucket
    num_buckets = size
    bucket_range = (global_max_val - global_min_val + 1) / num_buckets

    # Initialize the buckets
    buckets = [[] for _ in range(num_buckets)]

    # Assign elements to the buckets
    for num in local_arr:
        bucket_index = int((num - global_min_val) // bucket_range)
        buckets[bucket_index].append(num)

    # Gather all buckets to the root process
    gathered_buckets = comm.gather(buckets, root=0)

    # Concatenate the gathered buckets on the root process
    if rank == 0:
        sorted_arr = [num for bucket in gathered_buckets for sublist in bucket for num in sublist]
    else:
        sorted_arr = None

    # Broadcast the sorted array from the root process to all other processes
    sorted_arr = comm.bcast(sorted_arr, root=0)

    return sorted_arr

if __name__ == '__main__':
    import random

    # Generate a random array of 5000 elements
    arr = [random.randint(1, 5000) for _ in range(5000)]

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("Unsorted array:", arr)
        print("*********************************************************************************************")

    # Start the timer
    start_time = time.time()

    # Perform parallel Bucket Sort
    sorted_arr = bucket_sort_parallel(arr)

    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the sorted array and elapsed time on the root process
    if rank == 0:
        # print("Sorted array:", sorted_arr)
        print()
        print("Elapsed time: %.6f seconds" % elapsed_time)

        # Calculate speedup and efficiency
        sequential_time = elapsed_time * comm.Get_size()
        speedup = sequential_time / elapsed_time
        efficiency = speedup / comm.Get_size()
        print("Speedup:", speedup)
        print("Efficiency:", efficiency)
