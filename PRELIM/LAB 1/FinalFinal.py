import time

# ========= READ DATA FROM FILE =========
numbers = []

# Get the path of data.txt in the same folder as this file
data_file = __file__.replace("FinalFinal.py", "data.txt")

with open(data_file, "r") as file:
    for line in file:
        numbers.append(int(line.strip()))

# ========= BUBBLE SORT (DESCENDING) =========
start_time = time.time()

n = len(numbers)
for i in range(n):
    for j in range(0, n - i - 1):
        if numbers[j] < numbers[j + 1]:  # descending
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

end_time = time.time()

# ========= OUTPUT =========
print("Sorted data (descending):")
for num in numbers:
    print(num)

print("\nTotal numbers sorted:", len(numbers))
print("Time spent (seconds):", end_time - start_time)
