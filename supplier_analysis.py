import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data = []


def add_supplier():
    supplier_name = supplier_entry.get()
    try:
        rating = float(rating_entry.get())
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return
    
    if supplier_name:
        data.append({"Supplier": supplier_name, "Rating": rating})
        supplier_list.insert(tk.END, f"{supplier_name}: {rating}")
        supplier_entry.delete(0, tk.END)
        rating_entry.delete(0, tk.END)
        update_statistics()
    else:
        messagebox.showerror("Invalid Input", "Supplier name cannot be empty.")

def update_statistics():
    if data:
        df = pd.DataFrame(data)
        avg_rating = df['Rating'].mean()
        supplier_count = len(df['Supplier'].unique())
        stats_label.config(text=f"Average Rating: {avg_rating:.2f} | Total Suppliers: {supplier_count}")
    else:
        stats_label.config(text="No data available.")

def show_graphs():
    if data:
        df = pd.DataFrame(data)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))  
        fig.tight_layout(pad=5.0) 

        sns.histplot(df['Rating'], bins=5, kde=True, color='skyblue', ax=axes[0])
        axes[0].set_title("Distribution of Ratings")
        axes[0].set_xlabel("Rating")
        axes[0].set_ylabel("Count")

        sns.barplot(x="Supplier", y="Rating", data=df, palette="viridis", ax=axes[1])
        axes[1].set_title("Average Rating per Supplier")
        axes[1].set_xlabel("Supplier")
        axes[1].set_ylabel("Rating")
        axes[1].tick_params(axis='x', rotation=45)  

        plt.show()
    else:
        messagebox.showinfo("No Data", "No data available to display graphs.")


def clear_data():
    global data
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
        data = []
        supplier_list.delete(0, tk.END)
        update_statistics()
        messagebox.showinfo("Success", "All data has been cleared.")


root = tk.Tk()
root.title("Supplier Ratings System")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Supplier Name:").grid(row=0, column=0, padx=5)
supplier_entry = tk.Entry(input_frame, width=30)
supplier_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Rating (1-5):").grid(row=1, column=0, padx=5)
rating_entry = tk.Entry(input_frame, width=30)
rating_entry.grid(row=1, column=1, padx=5)

add_button = tk.Button(input_frame, text="Add Supplier", command=add_supplier)
add_button.grid(row=2, columnspan=2, pady=10)


list_frame = tk.Frame(root)
list_frame.pack(pady=10)

tk.Label(list_frame, text="Suppliers:").pack()
supplier_list = tk.Listbox(list_frame, width=50, height=10)
supplier_list.pack()


stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

stats_label = tk.Label(stats_frame, text="No data available.")
stats_label.pack()


buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

graphs_button = tk.Button(buttons_frame, text="Show Graphs", command=show_graphs)
graphs_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(buttons_frame, text="Clear Data", command=clear_data)
clear_button.grid(row=0, column=1, padx=5)

root.mainloop()