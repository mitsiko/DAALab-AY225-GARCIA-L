import time

# ========= MESSAGE BEFORE START =========
print("\nStarting timer... Loading data and sorting.")

# ========= START TIMER =========
start_time = time.time()

# ========= READ DATA FROM FILE =========
numbers = []

# Get the directory where this script is located
script_dir = __file__.rsplit("\\", 1)[0]
data_file = script_dir + "\\data.txt"

with open(data_file, "r") as file:
    for line in file:
        numbers.append(int(line.strip()))

# ========= BUBBLE SORT (DESCENDING) =========
n = len(numbers)
for i in range(n):
    for j in range(0, n - i - 1):
        if numbers[j] < numbers[j + 1]:  # descending
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

# ========= OUTPUT =========
print("Sorted data (descending):")
for num in numbers:
    print(num)

print("\nTotal numbers sorted:", len(numbers))

# ========= END TIMER =========
end_time = time.time()
print("Time spent (seconds):", end_time - start_time)
