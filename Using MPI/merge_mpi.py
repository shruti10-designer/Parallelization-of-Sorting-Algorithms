from mpi4py import MPI
import time

def merge_sort_parallel(arr):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Split the array into equal parts
    local_size = len(arr) // size
    local_arr = arr[rank * local_size: (rank + 1) * local_size]

    # Perform local merge sort
    local_sorted = merge_sort(local_arr)

    # Perform tree-based merge to obtain the final sorted array
    sorted_arr = tree_merge(local_sorted, comm)

    return sorted_arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

def tree_merge(local_arr, comm):
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Perform tree-based merge
    for i in range(int(size / 2)):
        partner = rank ^ (2 ** i)
        if rank < partner:
            partner_data = comm.recv(source=partner)
            local_arr = merge(local_arr, partner_data)
        else:
            comm.send(local_arr, dest=partner)

    return local_arr

if __name__ == '__main__':
    import random

    # Generate a random array of 1000 elements
    arr = [random.randint(1, 1000) for _ in range(1000)]

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("Unsorted array:", arr)
        print("********************************************************************")

    # Start the timer
    start_time = time.time()

    # Perform parallel Merge Sort
    sorted_arr = merge_sort_parallel(arr)

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
        if elapsed_time != 0:
            sequential_time = elapsed_time * comm.Get_size()
            speedup = sequential_time / elapsed_time
            efficiency = speedup / comm.Get_size()
            print("Speedup:", speedup)
            print("Efficiency:", efficiency)
        else:
            print("Elapsed time is zero, cannot calculate speedup and efficiency.")

