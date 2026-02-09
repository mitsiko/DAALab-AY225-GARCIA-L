"""
Benchmark logging module for storing and managing comparison results.
"""


class BenchmarkLogger:
    """Manages logging and storage of benchmark results."""
    
    def __init__(self):
        """Initialize the benchmark logger."""
        self.entries = []
    
    def add_entry(self, results):
        """
        Add a new benchmark entry.
        
        Args:
            results: Dictionary containing benchmark results
        """
        entry = {
            'algorithm': results['algorithm'],
            'num_rows': results['num_rows'],
            'sort_by': results['sort_by'],
            'load_time': results['load_time'],
            'sort_time': results['sort_time'],
            'total_time': results['total_time']
        }
        
        self.entries.append(entry)
    
    def clear_entries(self):
        """Clear all benchmark entries."""
        self.entries = []
    
    def get_entries(self):
        """
        Get all benchmark entries.
        
        Returns:
            list: List of all benchmark entries
        """
        return self.entries.copy()