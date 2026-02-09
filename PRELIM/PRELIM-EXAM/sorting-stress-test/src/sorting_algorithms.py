"""
Implementation of sorting algorithms from scratch.
No built-in sorting functions or libraries are used.
"""

import time
import copy


class SortingAlgorithms:
    """Contains implementations of various sorting algorithms."""
    
    def __init__(self):
        """Initialize the sorting algorithms class."""
        self.comparison_count = 0
        self.swap_count = 0
    
    def _reset_counts(self):
        """Reset comparison and swap counters."""
        self.comparison_count = 0
        self.swap_count = 0
    
    def _compare(self, a, b, sort_by):
        """
        Compare two records based on the specified column.
        
        Args:
            a, b: Dictionaries containing record data
            sort_by: Column name to sort by ('ID', 'FirstName', 'LastName')
        
        Returns:
            int: Negative if a < b, 0 if a == b, positive if a > b
        """
        self.comparison_count += 1
        
        if sort_by == 'ID':
            return a[sort_by] - b[sort_by]
        else:
            # String comparison
            if a[sort_by] < b[sort_by]:
                return -1
            elif a[sort_by] > b[sort_by]:
                return 1
            else:
                return 0
    
    # ========== BUBBLE SORT (O(n²)) ==========
    def bubble_sort(self, data, sort_by, progress_callback=None):
        """
        Bubble Sort implementation.
        
        Args:
            data: List of dictionaries to sort
            sort_by: Column to sort by
            progress_callback: Function to call with progress updates
        
        Returns:
            tuple: (sorted_data, number_of_operations)
        """
        self._reset_counts()
        n = len(data)
        arr = copy.deepcopy(data)
        
        # Total comparisons in Bubble Sort: n*(n-1)/2
        total_comparisons = n * (n - 1) // 2
        
        for i in range(n):
            swapped = False
            
            for j in range(0, n - i - 1):
                # Update progress based on completed comparisons
                if progress_callback:
                    # Calculate completed comparisons so far
                    # Comparisons completed in previous passes: i*(2*n - i - 1)//2
                    # Plus comparisons in current pass: j
                    completed = (i * (2 * n - i - 1) // 2) + j
                    progress = int((completed / total_comparisons) * 100)
                    # Update at reasonable intervals to avoid GUI overhead
                    if j % max(1, (n - i - 1) // 100) == 0:
                        progress_callback(min(99, progress))
                
                if self._compare(arr[j], arr[j + 1], sort_by) > 0:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swap_count += 1
                    swapped = True
            
            # If no swaps, array is already sorted
            if not swapped:
                # Update to 100% since we're done early
                if progress_callback:
                    progress_callback(100)
                break
        
        if progress_callback:
            progress_callback(100)
        
        return arr
    
    # ========== INSERTION SORT (O(n²)) ==========
    def insertion_sort(self, data, sort_by, progress_callback=None):
        """
        Insertion Sort implementation.
        
        Args:
            data: List of dictionaries to sort
            sort_by: Column to sort by
            progress_callback: Function to call with progress updates
        
        Returns:
            tuple: (sorted_data, number_of_operations)
        """
        self._reset_counts()
        arr = copy.deepcopy(data)
        n = len(arr)
        
        # In Insertion Sort, element i requires up to i comparisons in worst case
        # Total worst-case comparisons: n*(n-1)/2 (same as Bubble Sort)
        total_comparisons = n * (n - 1) // 2
        completed_comparisons = 0
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            # Count comparisons for this element
            element_comparisons = 0
            
            while j >= 0 and self._compare(arr[j], key, sort_by) > 0:
                arr[j + 1] = arr[j]
                self.swap_count += 1
                j -= 1
                element_comparisons += 1
            
            arr[j + 1] = key
            completed_comparisons += element_comparisons
            
            # Update progress
            if progress_callback:
                progress = int((completed_comparisons / total_comparisons) * 100)
                # Update at reasonable intervals
                if i % max(1, n // 100) == 0:
                    progress_callback(min(99, progress))
        
        if progress_callback:
            progress_callback(100)
        
        return arr
    
    # ========== MERGE SORT (O(n log n)) ==========
    def merge_sort(self, data, sort_by, progress_callback=None):
        """
        Merge Sort implementation.
        
        Args:
            data: List of dictionaries to sort
            sort_by: Column to sort by
            progress_callback: Function to call with progress updates
        
        Returns:
            tuple: (sorted_data, number_of_operations)
        """
        self._reset_counts()
        arr = copy.deepcopy(data)
        n = len(arr)
        
        # Merge Sort does approximately n*log2(n) comparisons
        # We'll track progress based on the merge operations
        self._merge_sort_total_work = 0
        self._merge_sort_completed = 0
        
        def _estimate_work(size):
            """Estimate total work for sorting size elements with merge sort."""
            # Each level divides by 2, total work ~ n*log2(n)
            if size <= 1:
                return 0
            return size + _estimate_work(size // 2) + _estimate_work(size - size // 2)
        
        # Estimate total work once
        if progress_callback:
            self._merge_sort_total_work = _estimate_work(n)
        
        def _merge_sort_recursive(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                
                # Recursively sort both halves
                _merge_sort_recursive(arr, left, mid)
                _merge_sort_recursive(arr, mid + 1, right)
                
                # Merge the sorted halves
                self._merge(arr, left, mid, right, sort_by)
                
                # Update progress after each merge
                if progress_callback:
                    # Each merge operation processes (right - left + 1) elements
                    self._merge_sort_completed += (right - left + 1)
                    progress = int((self._merge_sort_completed / self._merge_sort_total_work) * 100)
                    progress_callback(min(99, progress))
        
        _merge_sort_recursive(arr, 0, n - 1)
        
        if progress_callback:
            progress_callback(100)
        
        return arr
    
    def _merge(self, arr, left, mid, right, sort_by):
        """Helper function for Merge Sort."""
        n1 = mid - left + 1
        n2 = right - mid
        
        # Create temporary arrays
        left_arr = [arr[left + i] for i in range(n1)]
        right_arr = [arr[mid + 1 + i] for i in range(n2)]
        
        i = j = 0
        k = left
        
        # Merge the temporary arrays back
        while i < n1 and j < n2:
            if self._compare(left_arr[i], right_arr[j], sort_by) <= 0:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            self.swap_count += 1
            k += 1
        
        # Copy remaining elements
        while i < n1:
            arr[k] = left_arr[i]
            i += 1
            k += 1
        
        while j < n2:
            arr[k] = right_arr[j]
            j += 1
            k += 1
    
    # ========== MAIN SORTING INTERFACE ==========
    def sort_data(self, data, algorithm, sort_by, progress_callback=None):
        """
        Main method to sort data using the specified algorithm.
        
        Args:
            data: Data to sort
            algorithm: Name of algorithm ('Bubble Sort', 'Insertion Sort', 'Merge Sort')
            sort_by: Column to sort by
            progress_callback: Function for progress updates
        
        Returns:
            tuple: (sorted_data, sort_time)
        """
        start_time = time.time()
        
        if algorithm == 'Bubble Sort':
            sorted_data = self.bubble_sort(data, sort_by, progress_callback)
        elif algorithm == 'Insertion Sort':
            sorted_data = self.insertion_sort(data, sort_by, progress_callback)
        elif algorithm == 'Merge Sort':
            sorted_data = self.merge_sort(data, sort_by, progress_callback)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        sort_time = time.time() - start_time
        
        return sorted_data, sort_time