import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class NetflixVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Netflix Data Visualizer")
        self.root.geometry("800x650")
        
        # Apply a nicer theme if available
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        self.df = None
        self.figure = None
        self.canvas = None
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Top control frame
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)
        
        ttk.Label(control_frame, text="Select Column:", font=("Helvetica", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.column_var = tk.StringVar()
        self.column_cb = ttk.Combobox(control_frame, textvariable=self.column_var, state="readonly", width=25)
        self.column_cb.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="📊 Bar Chart", command=lambda: self.plot_graph("bar")).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🥧 Pie Chart", command=lambda: self.plot_graph("pie")).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📈 Histogram", command=lambda: self.plot_graph("hist")).pack(side=tk.LEFT, padx=5)
        
        # Plot frame
        self.plot_frame = ttk.Frame(self.root, padding=10)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
        
    def load_data(self):
        filename = "netflixdata.csv"
        try:
            # Check if file exists first to give a specific error message
            if not os.path.exists(filename):
                messagebox.showerror("File Error", f"Could not find '{filename}'. Please ensure it is in the same directory.")
                return

            self.df = pd.read_csv(filename, encoding='latin1')
            self.column_cb['values'] = list(self.df.columns)
            if self.df.columns.size > 0:
                self.column_cb.current(0)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading data:\n{str(e)}")

    def plot_graph(self, chart_type):
        if self.df is None:
            messagebox.showwarning("Warning", "Data not loaded!")
            return
            
        col = self.column_var.get()
        if not col or col not in self.df.columns:
            messagebox.showwarning("Warning", "Please select a valid column.")
            return

        data = self.df[col].dropna()
        
        if data.empty:
            messagebox.showwarning("Warning", f"The column '{col}' has no valid data.")
            return

        # Clear previous plot if any
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = self.figure.add_subplot(111)

        try:
            if chart_type == "pie":
                counts = data.value_counts().head(10)
                counts = counts[counts > 0] # ensure no 0 slices
                if counts.empty:
                    messagebox.showwarning("Warning", "No data to plot for pie chart.")
                    return
                
                # Shorten extremely long labels for the legend
                short_labels = [str(label)[:35] + '...' if len(str(label)) > 35 else str(label) for label in counts.index]
                
                # Remove direct outer labels, use a clean legend to prevent text overlap
                wedges, texts, autotexts = ax.pie(counts, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 9})
                ax.legend(wedges, short_labels, title="Categories", loc="center left", bbox_to_anchor=(0.9, 0.5), fontsize=9)
                ax.set_title(f"Top 10: {col} (Pie Chart)")
                ax.axis('equal')
                    
            elif chart_type == "bar":
                counts = data.value_counts().head(10)
                counts.plot(kind='bar', ax=ax, color='#1f77b4', edgecolor='black')
                ax.set_title(f"Top 10: {col} (Bar Chart)")
                ax.tick_params(axis='x', rotation=45)
                
            elif chart_type == "hist":
                numeric_data = pd.to_numeric(data, errors='coerce').dropna()
                
                # If more than half the data can be treated as numeric, plot a true distribution histogram
                if len(numeric_data) > 0.5 * len(data):
                    numeric_data.plot(kind='hist', ax=ax, bins=20, color='#2ca02c', edgecolor='black')
                    ax.set_title(f"Distribution of {col} (Histogram)")
                else:
                    # For text/categorical data, display a 'frequency histogram' of the top 10 items
                    counts = data.value_counts().head(10)
                    counts.plot(kind='bar', ax=ax, width=1.0, color='#2ca02c', edgecolor='black')
                    ax.set_title(f"Top 10 Frequencies: {col} (Categorical Histogram)")
                    ax.tick_params(axis='x', rotation=45)

            # Apply dynamic tight layout depending on the chart to make room for external legends
            if chart_type == "pie":
                self.figure.tight_layout(rect=[0, 0, 0.85, 1])
            else:
                self.figure.tight_layout()
            
            # Embed matplotlib figure in tkinter canvas
            self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Plot Error", f"Failed to plot graph:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetflixVisualizerApp(root)
    root.mainloop()
