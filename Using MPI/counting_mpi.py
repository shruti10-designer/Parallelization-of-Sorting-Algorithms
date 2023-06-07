from mpi4py import MPI
import time

def counting_sort_parallel(arr):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Split the array into equal parts
    local_size = len(arr) // size
    local_arr = arr[rank * local_size: (rank + 1) * local_size]

    # Perform counting sort locally
    local_sorted = counting_sort(local_arr)

    # Gather all locally sorted arrays to the root process
    gathered_arr = comm.gather(local_sorted, root=0)

    # Concatenate the gathered arrays on the root process
    if rank == 0:
        sorted_arr = [num for sublist in gathered_arr for num in sublist]
    else:
        sorted_arr = None

    return sorted_arr

def counting_sort(arr):
    count = [0] * (max(arr) + 1)
    for num in arr:
        count[num] += 1

    sorted_arr = []
    for i, freq in enumerate(count):
        sorted_arr.extend([i] * freq)

    return sorted_arr

if __name__ == '__main__':
    import random

    # Generate a random array of 5000 elements
    arr = [random.randint(1, 1000) for _ in range(5000)]

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("Unsorted array:", arr)
        print("**********************************************************************************")

    # Start the timer
    start_time = time.time()

    # Perform parallel Counting Sort
    sorted_arr = counting_sort_parallel(arr)

    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the sorted array and elapsed time on the root process
    if rank == 0:
        print("Sorted array:", sorted_arr)
        print()
        print("Elapsed time: %.6f seconds" % elapsed_time)
        

        # Calculate speedup and efficiency
        sequential_time = elapsed_time * comm.Get_size()
        speedup = sequential_time / elapsed_time
        efficiency = speedup / comm.Get_size()
        print("Speedup:", speedup)
        print("Efficiency:", efficiency)
