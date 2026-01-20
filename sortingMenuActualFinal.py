import time

# ==============================
# FUNCTION: Read data from file
# ==============================
def read_data(filename):
    numbers = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line != "":
                numbers.append(int(line))
    return numbers


# ==============================
# BUBBLE SORT
# ==============================
def bubble_sort(arr, ascending=True):
    data = arr.copy()
    n = len(data)

    start_time = time.time()

    for i in range(n):
        for j in range(0, n - i - 1):
            if ascending:
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
            else:
                if data[j] < data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]

    end_time = time.time()
    return data, end_time - start_time


# ==============================
# INSERTION SORT
# ==============================
def insertion_sort(arr, ascending=True):
    data = arr.copy()

    start_time = time.time()

    for i in range(1, len(data)):
        key = data[i]
        j = i - 1

        if ascending:
            while j >= 0 and data[j] > key:
                data[j + 1] = data[j]
                j -= 1
        else:
            while j >= 0 and data[j] < key:
                data[j + 1] = data[j]
                j -= 1

        data[j + 1] = key

    end_time = time.time()
    return data, end_time - start_time


# ==============================
# MERGE SORT
# ==============================
def merge_sort(arr, ascending=True):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], ascending)
    right = merge_sort(arr[mid:], ascending)

    return merge(left, right, ascending)


def merge(left, right, ascending):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if ascending:
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def timed_merge_sort(arr, ascending=True):
    data = arr.copy()

    start_time = time.time()
    sorted_data = merge_sort(data, ascending)
    end_time = time.time()

    return sorted_data, end_time - start_time


# ==============================
# MAIN PROGRAM (LOOPED)
# ==============================
def main():
    filename = "dataset.txt"
    numbers = read_data(filename)

    print("\nDATA LOADED SUCCESSFULLY")
    print("Total numbers:", len(numbers))

    while True:
        # ==================================
        # SORTING ALGORITHM MENU (VALIDATED)
        # ==================================
        while True:
            print("\n=== SORTING ALGORITHM MENU ===")
            print("1. Bubble Sort")
            print("2. Insertion Sort")
            print("3. Merge Sort")
            print("4. Exit Program")

            algo_choice = input("Enter your choice (1-4): ")

            if algo_choice in ["1", "2", "3", "4"]:
                break
            else:
                print("Invalid input. Please enter a number from 1 to 4.")

        if algo_choice == "4":
            print("\nProgram exited by user.")
            break

        # ================================
        # SORTING ORDER MENU (VALIDATED)
        # ================================
        while True:
            print("\n=== SORTING ORDER MENU ===")
            print("1. Ascending Order")
            print("2. Descending Order")

            order_choice = input("Enter your choice (1-2): ")

            if order_choice == "1":
                ascending = True
                order_name = "Ascending"
                break
            elif order_choice == "2":
                ascending = False
                order_name = "Descending"
                break
            else:
                print("Invalid input. Please enter 1 or 2.")

        # ================================
        # START TOTAL TIMING
        # ================================
        total_start_time = time.time()

        # ================================
        # EXECUTE SORTING
        # ================================
        if algo_choice == "1":
            sorted_data, _ = bubble_sort(numbers, ascending)
            algo_name = "Bubble Sort"

        elif algo_choice == "2":
            sorted_data, _ = insertion_sort(numbers, ascending)
            algo_name = "Insertion Sort"

        elif algo_choice == "3":
            sorted_data, _ = timed_merge_sort(numbers, ascending)
            algo_name = "Merge Sort"

        # ================================
        # DISPLAY SORTED DATA
        # ================================
        print("\nSorted Data:")
        for num in sorted_data:
            print(num)

        # ================================
        # DISPLAY RESULTS
        # ================================
        print("\n=== SORT RESULT ===")
        print("Sorting Algorithm:", algo_name)
        print("Sorting Order:", order_name)
        print("Number of elements sorted:", len(sorted_data))

        # ================================
        # END TOTAL TIMING
        # ================================
        total_end_time = time.time()
        total_time_spent = total_end_time - total_start_time

        print("Time taken (seconds):", total_time_spent)


# Run the program
main()
