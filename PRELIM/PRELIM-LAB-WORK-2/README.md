# Sorting Algorithm Console Program

## Overview
This is a **console-based Python program** that allows the user to sort a dataset of numbers using one of three sorting algorithms:  

1. **Bubble Sort**  
2. **Insertion Sort**  
3. **Merge Sort**  

Users can also select the sorting order: **Ascending** or **Descending**.  

The program measures the total time taken to **load the dataset, sort it, and display the sorted results**.  

The dataset is read from a text file named `dataset.txt` located in the **same directory** as this Python script.  

Additionally, the program now allows **dynamic dataset size selection**: the user can choose how many numbers from the dataset to sort. The program validates the input to ensure it does not exceed the number of available numbers in the dataset.

---

## Features
- Interactive console menu to choose sorting algorithm and order.  
- Dynamic dataset size selection: users can sort a subset of the dataset.  
- Measures time taken for **loading, sorting, and displaying** the dataset.  
- Works with datasets of any size (limited by your system memory).  
- Displays the sorted dataset directly in the console.  
- Input validation ensures only valid dataset sizes are accepted.  

---

## Requirements
- Python 3.x installed on your system.  
- A text file named `dataset.txt` in the same folder as the script. Each line in the file should contain a single integer. Example:

``` 
34
12
7
45
23
```

---

## How to Run

1. Open a terminal (Command Prompt, PowerShell, or Terminal app).  
2. Navigate to the folder containing the Python script and `dataset.txt`.  
3. Run the script using the following command:

```bash
python <script_name>.py
