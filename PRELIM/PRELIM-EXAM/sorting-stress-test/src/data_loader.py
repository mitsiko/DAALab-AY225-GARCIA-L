"""
Data loading module for reading and parsing CSV files.
Handles file path resolution and data type conversion.
"""

import csv
import os
import time


class DataLoader:
    """Handles loading and parsing of CSV data."""
    
    def __init__(self):
        """Initialize the data loader."""
        self.last_load_time = 0
        self._project_root = None
    
    def _get_project_root(self):
        """Dynamically determine the project root directory."""
        if self._project_root is None:
            # Get the directory of this file (data_loader.py)
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Go up one level to get src directory, then up again to get project root
            src_dir = os.path.dirname(current_file_dir)
            self._project_root = os.path.dirname(src_dir)
        
        return self._project_root
    
    def _get_csv_path(self):
        """Get the absolute path to the CSV file."""
        project_root = self._get_project_root()
        csv_path = os.path.join(project_root, 'data', 'generated_data.csv')
        
        # Check if file exists
        if not os.path.exists(csv_path):
            # Try alternative location (for direct execution)
            alt_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'generated_data.csv')
            csv_path = os.path.abspath(alt_path)
            
            if not os.path.exists(csv_path):
                raise FileNotFoundError(
                    f"CSV file not found. Tried:\n"
                    f"1. {os.path.join(project_root, 'data', 'generated_data.csv')}\n"
                    f"2. {csv_path}\n"
                    f"Please ensure the data/ directory contains generated_data.csv"
                )
        
        return csv_path
    
    def load_data(self):
        """
        Load and parse the CSV file.
        
        Returns:
            list: List of dictionaries containing the data
        """
        start_time = time.time()
        data = []
        
        try:
            csv_path = self._get_csv_path()
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row in csv_reader:
                    # Convert ID to integer
                    try:
                        row['ID'] = int(row['ID'])
                    except ValueError:
                        # If ID can't be converted to int, keep as string
                        pass
                    
                    data.append(row)
            
            self.last_load_time = time.time() - start_time
            return data
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return []
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []