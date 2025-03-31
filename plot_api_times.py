import pandas as pd
import matplotlib.pyplot as plt

def plot_api_times(csv_filepath):
    # Read data from the CSV file
    data = pd.read_csv(csv_filepath)
    
    # Group data by API Name
    grouped = data.groupby("API Name")
    
    # Plot all API times in the same plot
    plt.figure(figsize=(12, 6))
    for api_name, group in grouped:
        plt.plot(group["Iteration"], group["Time (seconds)"], label=api_name)
    
    # Add labels, title, and legend
    plt.xlabel("Iteration")
    plt.ylabel("Time (seconds)")
    plt.title("API Performance Over Iterations")
    plt.legend()
    plt.grid(True)
    
    # Show the plot
    plt.savefig("api_performance_plot.png")

if "__main__" == __name__:
    plot_api_times("api_test_results.csv")