from mpi4py import MPI
import time

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort_parallel(arr, low, high):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Split the array into equal parts
    local_size = len(arr) // size
    local_arr = arr[rank * local_size: (rank + 1) * local_size]

    # Perform local quicksort
    local_arr = quicksort(local_arr, 0, len(local_arr) - 1)

    # Gather all local arrays to the root process
    gathered_arr = comm.gather(local_arr, root=0)

    # Merge and sort the gathered arrays on the root process
    if rank == 0:
        sorted_arr = [item for sublist in gathered_arr for item in sublist]
        sorted_arr = quicksort(sorted_arr, 0, len(sorted_arr) - 1)
        return sorted_arr
    else:
        return None

def quicksort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)
    return arr

if __name__ == '__main__':
    import random

    # Generate a random array of 5000 elements
    arr = [random.randint(1, 1000) for _ in range(5000)]

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("Unsorted array:", arr)
        print("****************************************************************************************")

    # Start the timer
    start_time = time.time()

    # Perform parallel Quicksort
    sorted_arr = quicksort_parallel(arr, 0, len(arr) - 1)

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
