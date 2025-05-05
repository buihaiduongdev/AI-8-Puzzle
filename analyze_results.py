import json
import os
import matplotlib.pyplot as plt
import numpy as np 

def plot_results(json_filepath="result.json"):
    """
    Reads comparison results from JSON and generates plots using Matplotlib.

    Args:
        json_filepath (str): Path to the JSON results file.
    """
    print(f"\n--- Plotting Results from {json_filepath} ---")

    if not os.path.exists(json_filepath):
        print(f"Error: Results file not found at '{json_filepath}'")
        print("Please run the 'Compare All' function first.")
        print("--- Plotting End ---")
        return

    try:
        with open(json_filepath, 'r') as f:
            results_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_filepath}'. File might be corrupted.")
        print("--- Plotting End ---")
        return
    except Exception as e:
        print(f"Error reading file '{json_filepath}': {e}")
        print("--- Plotting End ---")
        return

    if not isinstance(results_data, dict) or not results_data:
        print("Error: JSON data is empty or not in the expected dictionary format.")
        print("--- Plotting End ---")
        return

    successful_runs_plot = []
    failed_algo_names = []

    for algo_name, details in results_data.items():
        if not isinstance(details, dict):
            print(f"Warning: Skipping invalid data format for algorithm '{algo_name}'")
            continue

        is_success = details.get("final_status", "Unknown") == "Success"
        if details.get("final_status") is None: 
             is_success = details.get("solve_time", -1.0) >= 0.0

        if is_success:
            solve_time = details.get("solve_time", None)
            path_length = details.get("path_length", None)

            if solve_time is not None and solve_time >= 0:
                 successful_runs_plot.append({
                     "name": algo_name,
                     "time": float(solve_time),

                     "length": int(path_length) if isinstance(path_length, (int, float)) else None,
                 })
        else:
            failed_algo_names.append(algo_name)

    if not successful_runs_plot:
        print("No successful runs found in the results file to plot.")
        if failed_algo_names:
             print(f"Failed algorithms: {', '.join(failed_algo_names)}")
        print("--- Plotting End ---")
        return

    successful_runs_plot.sort(key=lambda x: x['name'])
    algo_names = [run['name'] for run in successful_runs_plot]
    solve_times = [run['time'] for run in successful_runs_plot]

    runs_with_lengths = [run for run in successful_runs_plot if run['length'] is not None]
    path_lengths = [run['length'] for run in runs_with_lengths]
    names_with_lengths = [run['name'] for run in runs_with_lengths]

    num_plots = 1 + (1 if names_with_lengths else 0) 
    fig, axes = plt.subplots(nrows=num_plots, ncols=1, figsize=(10, 5 * num_plots), squeeze=False) 
    ax1 = axes[0, 0] 

    y_pos = np.arange(len(algo_names))
    bars1 = ax1.barh(y_pos, solve_times, align='center', color='skyblue')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(algo_names)
    ax1.invert_yaxis()  
    ax1.set_xlabel('Solve Time (seconds)')
    ax1.set_title('Algorithm Solve Time Comparison')
    ax1.grid(axis='x', linestyle='--', alpha=0.7)

    ax1.bar_label(bars1, fmt='%.4f', padding=3, fontsize=8)

    if names_with_lengths:
        ax2 = axes[1, 0] 
        y_pos_len = np.arange(len(names_with_lengths))
        bars2 = ax2.barh(y_pos_len, path_lengths, align='center', color='lightgreen')
        ax2.set_yticks(y_pos_len)
        ax2.set_yticklabels(names_with_lengths)
        ax2.invert_yaxis()
        ax2.set_xlabel('Path Length (steps)')
        ax2.set_title('Algorithm Path Length Comparison (Successful Runs)')
        ax2.grid(axis='x', linestyle='--', alpha=0.7)

        ax2.bar_label(bars2, fmt='%d', padding=3, fontsize=8) 
    elif num_plots > 1 :

         axes[1,0].set_visible(False)
         print("\nNote: No valid path length data found for successful runs to plot.")

    plt.tight_layout(pad=2.0) 
    print("Displaying plots...")
    plt.show() 

    if failed_algo_names:
        print(f"\nNote: The following algorithms failed or were excluded due to errors: {', '.join(failed_algo_names)}")

    print("--- Plotting End ---")

if __name__ == "__main__":

    plot_results() 