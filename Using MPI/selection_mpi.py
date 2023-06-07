from mpi4py import MPI
import time

def selection_sort_parallel(arr):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Split the array into equal parts
    local_size = len(arr) // size
    local_arr = arr[rank * local_size: (rank + 1) * local_size]

    # Perform local selection sort
    for i in range(local_size):
        min_index = i
        for j in range(i + 1, local_size):
            if local_arr[j] < local_arr[min_index]:
                min_index = j
        local_arr[i], local_arr[min_index] = local_arr[min_index], local_arr[i]

    # Gather all local arrays to the root process
    gathered_arr = comm.gather(local_arr, root=0)

    # Merge and sort the gathered arrays on the root process
    if rank == 0:
        sorted_arr = [item for sublist in gathered_arr for item in sublist]
        for i in range(len(sorted_arr)):
            min_index = i
            for j in range(i + 1, len(sorted_arr)):
                if sorted_arr[j] < sorted_arr[min_index]:
                    min_index = j
            sorted_arr[i], sorted_arr[min_index] = sorted_arr[min_index], sorted_arr[i]
        return sorted_arr
    else:
        return None

if __name__ == '__main__':
    import random

    # Generate a random array of 5000 elements
    arr = [random.randint(1, 5000) for _ in range(5000)]

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("Unsorted array:", arr)
        print("****************************************************************************************")

    # Start the timer
    start_time = time.time()

    # Perform parallel Selection Sort
    sorted_arr = selection_sort_parallel(arr)

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
