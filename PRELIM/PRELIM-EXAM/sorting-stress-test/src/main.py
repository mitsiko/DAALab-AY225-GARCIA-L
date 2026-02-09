#!/usr/bin/env python3
"""
Main entry point for the Sorting Algorithm Stress Test application.
Handles GUI initialization and coordinates between modules.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add project root to path for module imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data_loader import DataLoader
from src.sorting_algorithms import SortingAlgorithms
from src.gui_components import GUIComponents
from src.benchmark_logger import BenchmarkLogger


class SortingStressTestApp:
    """Main application class that coordinates all components."""
    
    def __init__(self):
        """Initialize the application and GUI."""
        self.root = tk.Tk()
        self.root.title("Sorting Algorithm Stress Test - University Prelim Exam")
        
        # Set window size to 75% width and 90% height of screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.90)
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"+{x_position}+{y_position}")
        
        # Set minimum size constraints
        min_width = 1200  # Enough to prevent text truncation
        min_height = int(screen_height * 0.50)  # 50% of screen height
        self.root.minsize(width=min_width, height=min_height)
        
        # Initialize components
        self.data_loader = DataLoader()
        self.sorting_algs = SortingAlgorithms()
        self.benchmark_logger = BenchmarkLogger()
        
        # Initialize GUI
        self.gui = GUIComponents(self.root, self)
        
        # State variables
        self.original_data = []
        self.current_results = None
        self.is_loading = False
        self.is_sorting = False
        
        # Set up closing handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Handle window closing event."""
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()
    
    def start_sorting(self, algorithm, sort_by, num_rows):
        """Main sorting execution handler."""
        try:
            # Clear previous results and show sorting in progress
            self.gui.clear_results_display()
            self.gui.show_sorting_in_progress()
            
            # Validate inputs
            num_rows = int(num_rows)
            if num_rows <= 0:
                messagebox.showerror("Invalid Input", "Number of rows must be positive")
                self.gui.hide_sorting_in_progress()
                return
            
            # Check if O(n²) algorithm with large N
            if algorithm in ["Bubble Sort", "Insertion Sort"] and num_rows >= 50000:
                response = messagebox.askyesno(
                    "Performance Warning",
                    f"{algorithm} is O(n²) and may take a long time with {num_rows:,} rows.\n"
                    "Do you want to continue?"
                )
                if not response:
                    self.gui.hide_sorting_in_progress()
                    return
            
            # Update GUI state
            self.gui.set_loading_state(True)
            self.gui.update_status("Loading data...")
            
            # Load data (with fresh copy each time)
            self.original_data = self.data_loader.load_data()
            if not self.original_data:
                messagebox.showerror("Data Error", "Failed to load data")
                self.gui.set_loading_state(False)
                self.gui.hide_sorting_in_progress()
                return
            
            # Check if enough data
            if num_rows > len(self.original_data):
                messagebox.showerror(
                    "Insufficient Data",
                    f"Requested {num_rows} rows, but only {len(self.original_data)} available"
                )
                self.gui.set_loading_state(False)
                self.gui.hide_sorting_in_progress()
                return
            
            # Get subset of data
            data_to_sort = self.original_data[:num_rows]
            
            # Update GUI for sorting
            self.gui.update_status("Sorting data...")
            
            # Perform sorting
            sorted_data, sort_time = self.sorting_algs.sort_data(
                data_to_sort.copy(),  # Fresh copy for each sort
                algorithm,
                sort_by,
                progress_callback=self.gui.update_progress
            )
            
            # Update GUI with results
            self.gui.update_status("")
            self.gui.set_loading_state(False)
            
            # Store results
            self.current_results = {
                'algorithm': algorithm,
                'sort_by': sort_by,
                'num_rows': num_rows,
                'load_time': self.data_loader.last_load_time,
                'sort_time': sort_time,
                'total_time': self.data_loader.last_load_time + sort_time,
                'sorted_data': sorted_data
            }
            
            # Display results
            self.gui.display_results(self.current_results)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of rows must be a valid integer")
            self.gui.set_loading_state(False)
            self.gui.hide_sorting_in_progress()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.gui.set_loading_state(False)
            self.gui.hide_sorting_in_progress()
    
    def log_to_comparison_table(self):
        """Log current results to comparison table."""
        if self.current_results:
            self.benchmark_logger.add_entry(self.current_results)
            self.gui.update_comparison_table(self.benchmark_logger.entries)
    
    def clear_comparison_table(self):
        """Clear all entries from comparison table."""
        if messagebox.askyesno(
            "Clear Table",
            "Are you sure you want to clear all logged benchmark results?"
        ):
            self.benchmark_logger.clear_entries()
            self.gui.update_comparison_table(self.benchmark_logger.entries)
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()


def main():
    """Application entry point."""
    app = SortingStressTestApp()
    app.run()


if __name__ == "__main__":
    main()