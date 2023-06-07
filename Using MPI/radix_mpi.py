from mpi4py import MPI
import time

def radix_sort_parallel(arr):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Determine the maximum number of digits in the array
    max_digits = comm.allreduce(len(str(max(arr))), op=MPI.MAX)

    # Perform radix sort for each digit position
    for digit_pos in range(max_digits):
        # Split the array into equal parts
        local_size = len(arr) // size
        local_arr = arr[rank * local_size: (rank + 1) * local_size]

        # Perform counting sort based on the current digit position
        local_arr = counting_sort_digit(local_arr, digit_pos)

        # Gather all locally sorted arrays to the root process
        gathered_arr = comm.gather(local_arr, root=0)

        # Concatenate the gathered arrays on the root process
        if rank == 0:
            arr = [num for sublist in gathered_arr for num in sublist]

        # Broadcast the updated array from the root process to all other processes
        arr = comm.bcast(arr, root=0)

    return arr

def counting_sort_digit(arr, digit_pos):
    count = [0] * 10
    for num in arr:
        digit = (num // 10**digit_pos) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    sorted_arr = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        digit = (num // 10**digit_pos) % 10
        count[digit] -= 1
        sorted_arr[count[digit]] = num

    return sorted_arr


if __name__ == '__main__':
    import random

    # Generate a random array of 1000 elements
    arr = [random.randint(1, 1000) for _ in range(5000)]

    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("Unsorted array:", arr)
        print("*********************************************************************************")

    # Start the timer
    start_time = time.time()

    # Perform parallel Radix Sort
    sorted_arr = radix_sort_parallel(arr)

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

