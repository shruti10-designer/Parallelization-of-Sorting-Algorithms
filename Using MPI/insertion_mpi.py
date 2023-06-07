from mpi4py import MPI
import time

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def insertion_sort_parallel(arr):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Split the array into equal parts
    local_size = len(arr) // size
    local_arr = arr[rank * local_size: (rank + 1) * local_size]

    # Perform local insertion sort
    insertion_sort(local_arr)

    # Gather all locally sorted arrays to the root process
    gathered_arr = comm.gather(local_arr, root=0)

    # Concatenate the gathered arrays on the root process
    if rank == 0:
        sorted_arr = [num for sublist in gathered_arr for num in sublist]
    else:
        sorted_arr = None

    return sorted_arr

if __name__ == '__main__':
    import random

    # Generate a random array of 1000 elements
    arr = [random.randint(1, 5000) for _ in range(5000)]

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("Unsorted array:", arr)
        print("*****************************************************************************************")

    # Start the timer
    start_time = time.time()

    # Perform parallel Insertion Sort
    sorted_arr = insertion_sort_parallel(arr)

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
        sequential_time = elapsed_time
        speedup = sequential_time / elapsed_time
        efficiency = speedup / comm.Get_size()
        print("Speedup:", speedup)
        print("Efficiency:", efficiency)

