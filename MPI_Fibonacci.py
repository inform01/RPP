from mpi4py import MPI
import time
def read_input_file(file_name):
    """Читає одне ціле число N з вхідного файлу. Це число визначає верхню межу діапазону."""
    with open(file_name, 'r') as f:
        N = int(f.read().strip())
    return N

def write_output_file(file_name, fibonacci_numbers):
    """Записує кожне число Фібоначчі в окремий рядок вихідного файлу."""
    with open(file_name, 'w') as f:
        for number in fibonacci_numbers:
            f.write(f"{number}\n")

def is_fibonacci(n):
    """Перевіряє, чи є число n числом Фібоначчі."""
    if n < 0:
        return False
    a, b = 0, 1
    while b <= n:
        if b == n or a == n:
            return True
        a, b = b, a + b
    return False


def process_range(N, size):
    """Розподіляє діапазон чисел [0, N] між процесами."""
    chunk_size = (N + 1) // size
    ranges = [(i * chunk_size, min((i + 1) * chunk_size - 1, N)) for i in range(size)]
    return ranges

def main(input_file, output_file):
    start_time = time.time()

    comm = MPI.COMM_WORLD
    size = comm.Get_size()  # Кількість процесів у комунікаторі MPI
    rank = comm.Get_rank()  # Унікальний ідентифікатор (ранг) процесу у комунікаторі

    N = None
    if rank == 0:  # Кореневий процес читає вхідні дані і розподіляє задачі
        N = read_input_file(input_file)
        ranges = process_range(N, size)
    else:
        ranges = None

    # Розподіл діапазонів чисел між усіма процесами
    range_to_check = comm.scatter(ranges, root=0)

    # Обрахунок чисел Фібоначчі в заданому діапазоні
    local_fibonacci_numbers = [n for n in range(range_to_check[0], range_to_check[1] + 1) if is_fibonacci(n)]

    # Збір результатів від усіх процесів у кореневому процесі
    all_fibonacci_numbers = comm.gather(local_fibonacci_numbers, root=0)

    if rank == 0:
        # Об'єднання списків в один та запис у файл
        all_fibonacci_numbers = [num for sublist in all_fibonacci_numbers for num in sublist]
        write_output_file(output_file, all_fibonacci_numbers)
        print("Fibonacci numbers from your range were found and saved in the output file.")
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        print(f"Execution time: {total_time_ms:.2f} ms")

if __name__ == "__main__":
    input_file = "C:\MPI_fil\input.txt"
    output_file = "C:\MPI_fil\output.txt"
    main(input_file, output_file)

#mpiexec -n 2 python C:\Users\Сергій\PycharmProjects\pythonProject_MPI\MPI_Fibonacci.py