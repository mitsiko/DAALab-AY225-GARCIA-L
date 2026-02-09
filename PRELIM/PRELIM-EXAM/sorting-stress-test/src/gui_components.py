"""
GUI components for the sorting stress test application.
Implements all required UI elements using Tkinter.
"""

import tkinter as tk
from tkinter import ttk
import threading


class GUIComponents:
    """Manages all GUI components and layout."""
    
    def __init__(self, root, app):
        """
        Initialize GUI components.
        
        Args:
            root: Tkinter root window
            app: Reference to main application
        """
        self.root = root
        self.app = app
        
        # Configure monospace font
        self._configure_monospace_font()
        
        # Create main container with vertical scrollbar only
        self._create_scrollable_container()
        
        # Create all sections
        self._create_top_section()
        self._create_middle_section()
        self._create_bottom_section()
        
        # Configure scroll region
        self._configure_scroll_region()
        
        # Initial state
        self._reset_results_display()
    
    def _configure_monospace_font(self):
        """Configure all fonts to use monospace."""
        # Define monospace font
        self.mono_font = ('Courier New', 10)
        self.mono_bold_font = ('Courier New', 10, 'bold')
        self.mono_italic_font = ('Courier New', 10, 'italic')
        self.mono_bold_italic_font = ('Courier New', 10, 'bold', 'italic')
        
        # Configure ttk styles with monospace font
        style = ttk.Style()
        
        # Configure all widget styles to use monospace
        for style_name in ['TLabel', 'TButton', 'TEntry', 'TCombobox', 'TLabelframe', 'TLabelframe.Label']:
            style.configure(style_name, font=self.mono_font)
        
        # Configure Treeview with monospace
        style.configure("Treeview", 
                       font=self.mono_font,
                       rowheight=25)
        style.configure("Treeview.Heading",
                       font=self.mono_bold_font)
    
    def _create_scrollable_container(self):
        """Create a scrollable container for the entire GUI (vertical only)."""
        # Create main frame with vertical scrollbar only
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add vertical scrollbar only (NO horizontal scrollbar)
        v_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.main_canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure canvas with vertical scrolling only
        self.main_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        # Create frame inside canvas
        self.main_frame = ttk.Frame(self.main_canvas, padding="10")
        self.main_frame_id = self.main_canvas.create_window((0, 0), window=self.main_frame, anchor=tk.NW)
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        
        # Bind events for scrolling
        self.main_frame.bind('<Configure>', self._on_frame_configure)
        self.main_canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Bind mouse wheel for scrolling
        self._bind_mouse_wheel()
    
    def _bind_mouse_wheel(self):
        """Bind mouse wheel events for scrolling."""
        self.main_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.main_canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self.main_canvas.bind_all("<Button-5>", self._on_mouse_wheel)
    
    def _on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 5 or event.delta == -120:
            self.main_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.main_canvas.yview_scroll(-1, "units")
    
    def _on_frame_configure(self, event):
        """Update scroll region when frame size changes."""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Update canvas window width when canvas size changes."""
        # Set frame width to canvas width (no horizontal scrolling)
        self.main_canvas.itemconfig(self.main_frame_id, width=event.width)
    
    def _configure_scroll_region(self):
        """Configure the initial scroll region."""
        self.root.update_idletasks()
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def _create_top_section(self):
        """Create the top input section."""
        # Section frame
        top_frame = ttk.LabelFrame(self.main_frame, text="SORTING PARAMETERS", padding="15")
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=5, pady=(0, 10))
        top_frame.columnconfigure(1, weight=1)
        
        # Algorithm selection
        ttk.Label(top_frame, text="Algorithm:", font=self.mono_font).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5
        )
        self.algorithm_var = tk.StringVar(value="Merge Sort")
        self.algorithm_combo = ttk.Combobox(
            top_frame,
            textvariable=self.algorithm_var,
            values=["Bubble Sort", "Insertion Sort", "Merge Sort"],
            state="readonly",
            width=25,
            font=self.mono_font
        )
        self.algorithm_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Column selection
        ttk.Label(top_frame, text="Sort By:", font=self.mono_font).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5
        )
        self.column_var = tk.StringVar(value="ID")
        self.column_combo = ttk.Combobox(
            top_frame,
            textvariable=self.column_var,
            values=["ID", "FirstName", "LastName"],
            state="readonly",
            width=25,
            font=self.mono_font
        )
        self.column_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Number of rows input
        ttk.Label(top_frame, text="Number of Rows (N):", font=self.mono_font).grid(
            row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5
        )
        self.rows_var = tk.StringVar(value="1000")
        self.rows_entry = ttk.Entry(
            top_frame,
            textvariable=self.rows_var,
            width=25,
            font=self.mono_font
        )
        self.rows_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Start button
        self.start_button = ttk.Button(
            top_frame,
            text="Start Sorting",
            command=self._on_start_sorting,
            width=15
        )
        self.start_button.grid(row=0, column=2, rowspan=3, padx=(30, 0), pady=5)
        
        # Status label
        self.status_label = ttk.Label(
            top_frame,
            text="",
            font=self.mono_italic_font
        )
        self.status_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Progress indicator
        self.progress_label = ttk.Label(
            top_frame,
            text="",
            font=self.mono_bold_font
        )
        self.progress_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
    
    def _create_middle_section(self):
        """Create the middle results section."""
        # Section frame
        self.middle_frame = ttk.Frame(self.main_frame)
        self.middle_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=(0, 10))
        
        # Configure middle frame for 50/50 split
        self.middle_frame.columnconfigure(0, weight=1)
        self.middle_frame.columnconfigure(1, weight=1)
        self.middle_frame.rowconfigure(0, weight=1)
        
        # Results Statistics Panel (Left 50%)
        self.stats_frame = ttk.LabelFrame(self.middle_frame, text="RESULTS STATISTICS", padding="15")
        self.stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        self.stats_frame.columnconfigure(1, weight=1)
        
        # Results Table (Right 50%) - ALWAYS VISIBLE
        self.results_table_frame = ttk.LabelFrame(self.middle_frame, text="SORTED RECORDS (First 10)", padding="10")
        self.results_table_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        self.results_table_frame.columnconfigure(0, weight=1)
        self.results_table_frame.rowconfigure(0, weight=1)
        
        # Create statistics labels (will be populated when results are available)
        self._create_statistics_labels()
        
        # Create results table (always visible)
        self._create_results_table()
    
    def _create_statistics_labels(self):
        """Create labels for statistics display."""
        self.stat_labels = {}
        stat_names = [
            ("Algorithm:", "algorithm"),
            ("Column Sorted By:", "column"),
            ("Number of Rows:", "rows"),
            ("Data Loading Time:", "load_time"),
            ("Sorting Time:", "sort_time"),
            ("Total Execution Time:", "total_time")
        ]
        
        # Clear any existing widgets in stats_frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Create new labels
        for i, (label_text, key) in enumerate(stat_names):
            ttk.Label(self.stats_frame, text=label_text, font=self.mono_font).grid(
                row=i, column=0, sticky=tk.W, padx=(0, 10), pady=5
            )
            value_label = ttk.Label(
                self.stats_frame,
                text="",
                font=self.mono_font,
                foreground="#0066CC"
            )
            value_label.grid(row=i, column=1, sticky=tk.W, pady=5)
            self.stat_labels[key] = value_label
        
        # Sorting in progress label (initially hidden)
        self.sorting_progress_label = ttk.Label(
            self.stats_frame,
            text="",
            font=self.mono_bold_italic_font,
            foreground="#FF6600"
        )
        self.sorting_progress_label.grid(row=len(stat_names), column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # Log button
        self.log_button = ttk.Button(
            self.stats_frame,
            text="Log into Comparison Table",
            command=self.app.log_to_comparison_table,
            state=tk.DISABLED
        )
        self.log_button.grid(row=len(stat_names) + 1, column=0, columnspan=2, pady=(15, 0))
    
    def _create_results_table(self):
        """Create the results table widget (always visible)."""
        # Create Treeview with vertical scrollbar only
        self.results_tree_frame = ttk.Frame(self.results_table_frame)
        self.results_tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.results_tree_frame.columnconfigure(0, weight=1)
        self.results_tree_frame.rowconfigure(0, weight=1)
        
        # Create Treeview with explicitly sized columns to prevent horizontal overflow
        self.results_tree = ttk.Treeview(
            self.results_tree_frame,
            columns=('ID', 'FirstName', 'LastName'),
            show='headings',
            height=10
        )
        
        # Define columns with explicit widths (sum must fit within minimum window width)
        self.results_tree.heading('ID', text='ID')
        self.results_tree.heading('FirstName', text='First Name')
        self.results_tree.heading('LastName', text='Last Name')
        
        # Set column widths to fit within allocated space
        column_widths = {
            'ID': 120,
            'FirstName': 200,
            'LastName': 200
        }
        
        for col, width in column_widths.items():
            self.results_tree.column(col, width=width, anchor=tk.W)
        
        # Add vertical scrollbar only (NO horizontal scrollbar)
        v_scrollbar = ttk.Scrollbar(self.results_tree_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Grid everything
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure column stretching
        self.results_tree_frame.columnconfigure(0, weight=1)
    
    def _create_bottom_section(self):
        """Create the bottom benchmark comparison table section."""
        # Section frame
        bottom_frame = ttk.LabelFrame(self.main_frame, text="BENCHMARK COMPARISON TABLE", padding="10")
        bottom_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=(0, 10))
        
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(0, weight=1)
        
        # Create Treeview with vertical scrollbar only
        tree_frame = ttk.Frame(bottom_frame)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create Treeview with explicitly sized columns
        self.comparison_tree = ttk.Treeview(
            tree_frame,
            columns=('algorithm', 'rows', 'sort_by', 'load_time', 'sort_time', 'total_time'),
            show='headings',
            height=8
        )
        
        # Define columns with explicit widths to prevent horizontal overflow
        columns = [
            ('Algorithm Used', 170),
            ('Number of Rows', 150),
            ('Sorted By', 150),
            ('Loading Time (s)', 150),
            ('Sorting Time (s)', 250),
            ('Total Time (s)', 250)
        ]
        
        total_width = sum(width for _, width in columns)
        
        for col, (heading, width) in zip(self.comparison_tree['columns'], columns):
            self.comparison_tree.heading(col, text=heading)
            self.comparison_tree.column(col, width=width, anchor=tk.CENTER, stretch=False)
        
        # Add vertical scrollbar only (NO horizontal scrollbar)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.comparison_tree.yview)
        self.comparison_tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Grid everything
        self.comparison_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Clear button
        clear_button = ttk.Button(
            bottom_frame,
            text="Clear Comparison Table",
            command=self.app.clear_comparison_table,
            width=25
        )
        clear_button.grid(row=1, column=0, pady=(10, 0))
        
        # Update scroll region after creating bottom section
        self.root.after(100, self._configure_scroll_region)
    
    def _on_start_sorting(self):
        """Handle start sorting button click."""
        # Get values from UI
        algorithm = self.algorithm_var.get()
        sort_by = self.column_var.get()
        num_rows = self.rows_var.get()
        
        # Run sorting in a separate thread to keep UI responsive
        thread = threading.Thread(
            target=self.app.start_sorting,
            args=(algorithm, sort_by, num_rows),
            daemon=True
        )
        thread.start()
    
    def set_loading_state(self, loading):
        """
        Update UI state during loading/sorting.
        
        Args:
            loading: True if loading/sorting is in progress
        """
        self.is_loading = loading
        
        if loading:
            self.start_button.config(state=tk.DISABLED)
            self.algorithm_combo.config(state=tk.DISABLED)
            self.column_combo.config(state=tk.DISABLED)
            self.rows_entry.config(state=tk.DISABLED)
            self.log_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.algorithm_combo.config(state="readonly")
            self.column_combo.config(state="readonly")
            self.rows_entry.config(state=tk.NORMAL)
    
    def update_status(self, message):
        """
        Update status label.
        
        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def update_progress(self, percentage):
        """
        Update progress indicator.
        
        Args:
            percentage: Progress percentage (0-100)
        """
        if percentage < 100:
            self.progress_label.config(text=f"Progress: {percentage}%")
        else:
            self.progress_label.config(text="")
        self.root.update_idletasks()
    
    def clear_results_display(self):
        """Clear the results display area when starting new sort."""
        # Clear statistics labels
        for label in self.stat_labels.values():
            label.config(text="")
        
        # Clear results table (keep headers visible)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Clear sorting progress label
        self.sorting_progress_label.config(text="")
        
        # Disable log button
        self.log_button.config(state=tk.DISABLED)
        
        # Update UI
        self.root.update_idletasks()
    
    def show_sorting_in_progress(self):
        """Show sorting in progress message in statistics panel."""
        self.sorting_progress_label.config(text="Sorting...")
        self.root.update_idletasks()
    
    def hide_sorting_in_progress(self):
        """Hide sorting in progress message."""
        self.sorting_progress_label.config(text="")
        self.root.update_idletasks()
    
    def _reset_results_display(self):
        """Reset the results display area to initial state."""
        # Clear statistics labels
        for label in self.stat_labels.values():
            label.config(text="")
        
        # Clear results table (keep headers)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Clear sorting progress label
        self.sorting_progress_label.config(text="")
        
        # Disable log button initially
        self.log_button.config(state=tk.DISABLED)
        
        # Ensure Results Table is always visible in 50/50 split
        # (Already handled by grid configuration in __init__)
    
    def display_results(self, results):
        """
        Display sorting results.
        
        Args:
            results: Dictionary containing results data
        """
        # Hide sorting in progress message
        self.hide_sorting_in_progress()
        
        # Update statistics
        self.stat_labels['algorithm'].config(text=results['algorithm'])
        self.stat_labels['column'].config(text=results['sort_by'])
        self.stat_labels['rows'].config(text=f"{results['num_rows']:,}")
        self.stat_labels['load_time'].config(text=f"{results['load_time']:.4f} s")
        self.stat_labels['sort_time'].config(text=f"{results['sort_time']:.4f} s")
        self.stat_labels['total_time'].config(text=f"{results['total_time']:.4f} s")
        
        # Update results table (keep headers visible)
        self._update_results_table(results['sorted_data'][:10])
        
        # Enable log button
        self.log_button.config(state=tk.NORMAL)
        
        # Update scroll region
        self._configure_scroll_region()
    
    def _update_results_table(self, data):
        """Update the results table with sorted data."""
        # Clear existing items (keep headers)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Insert new data
        for record in data:
            self.results_tree.insert('', tk.END, values=(
                record['ID'],
                record['FirstName'],
                record['LastName']
            ))
    
    def update_comparison_table(self, entries):
        """Update the benchmark comparison table."""
        # Clear existing items
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        
        # Insert new entries
        for entry in entries:
            self.comparison_tree.insert('', tk.END, values=(
                entry['algorithm'],
                f"{entry['num_rows']:,}",
                entry['sort_by'],
                f"{entry['load_time']:.4f}",
                f"{entry['sort_time']:.4f}",
                f"{entry['total_time']:.4f}"
            ))
        
        # Update scroll region
        self._configure_scroll_region()