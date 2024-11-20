import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from tkinter import messagebox, filedialog
import tkinter as tk


df = None

def load_data_from_excel():
    global df
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", ".xlsx;.xls")])
    if file_path:
        try:
            df = pd.read_excel(file_path, index_col=0, parse_dates=True)
            messagebox.showinfo("Success", "Data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    else:
        messagebox.showerror("Error", "No file selected.")

def train_and_predict():
    global df
    if df is None:
        messagebox.showerror("Error", "No data loaded. Please load a valid Excel file.")
        return
    
    
    train_size = int(len(df) * 0.8)
    train, test = df['Orders'][:train_size], df['Orders'][train_size:]

    try:
      
        model = ARIMA(train, order=(1, 1, 1))  # (p, d, q)
        model_fit = model.fit()

        forecast = model_fit.forecast(steps=len(test))

        plt.figure(figsize=(10, 6))
        plt.plot(df['Orders'], label="Actual Orders")
        plt.plot(test.index, forecast, label="Forecasted Orders", color='red')
        plt.title("Order Forecasting with ARIMA")
        plt.xlabel("Date")
        plt.ylabel("Orders")
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Model training failed: {str(e)}")

def create_gui():
    root = tk.Tk()
    root.title("Order Forecasting System")

    
    load_button = tk.Button(root, text="Load Data from Excel", command=load_data_from_excel)
    load_button.pack(pady=20)

   
    forecast_button = tk.Button(root, text="Predict Orders", command=train_and_predict)
    forecast_button.pack(pady=20)

    root.mainloop()

create_gui()