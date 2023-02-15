import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_stats(data):
    """
    Calculate the median, mean, max, and min of the CPU and memory usage.
    """
    cpu_median = data["cpu_usage_avg"].median()
    cpu_mean = data["cpu_usage_avg"].mean()
    cpu_max = data["cpu_usage_avg"].max()
    cpu_min = data["cpu_usage_avg"].min()

    mem_median = data["memory_usage_avg"].median()
    mem_mean = data["memory_usage_avg"].mean()
    mem_max = data["memory_usage_avg"].max()
    mem_min = data["memory_usage_avg"].min()

    return [cpu_median, cpu_mean, cpu_max, cpu_min, mem_median, mem_mean, mem_max, mem_min]

def get_latency_stats(data):
    """
    Calculate the median, mean, max, and min of the latency.
    """
    latency_median = data["Latency"].median()
    latency_mean = data["Latency"].mean()
    latency_max = data["Latency"].max()
    latency_min = data["Latency"].min()

    return [latency_median, latency_mean, latency_max, latency_min]

def get_latency_data(hpa_cpu_threshold):
    """
    Returns a list of latency values from the JMeter test results CSV file.
    """
    # Create the file name
    filename = os.path.join("..", "JmeterLoadTest", "REPORT_HTML{}".format(hpa_cpu_threshold), "results.csv")
    
    # Load the data from the CSV file
    data = pd.read_csv(filename)
    
    # Filter the data to include only the "HTTP Request API" rows
    filtered_data = data[data["label"] == "HTTP Request API"]
    
    # Return the latency data
    return filtered_data


def main():
    """
    Main function to draw boxplots of the CPU and memory usage.
    """
    # Define the command-line arguments
    parser = argparse.ArgumentParser(description="Draw boxplots of the CPU and memory usage")
    parser.add_argument("--filename", type=str, default="deployment_metrics.csv", help="The input file name")
    parser.add_argument("--latency", action='store_true', help="Draw boxplots of the HTTP Request API latencies")
    args = parser.parse_args()

    # Load the data from the CSV file
    data = pd.read_csv(args.filename)

    # Get the unique values of the hpa_cpu_threshold
    unique_thresholds = data["hpa_cpu_threshold"].unique()

    fontsize=7

    # Draw the boxplots of the CPU usage
    fig, ax = plt.subplots(2+ args.latency, 1, figsize=(10, 10))
    cpu_thresholds = []
    cpu_means = []
    for i, hpa_cpu_threshold in enumerate(unique_thresholds):
        # Filter the data for the current hpa_cpu_threshold
        filtered_data = data[data["hpa_cpu_threshold"] == hpa_cpu_threshold]

        # Draw the boxplot of the CPU usage
        box = filtered_data.boxplot(column="cpu_usage_avg", ax=ax[0], positions=[i], return_type="dict")
        stats = get_stats(filtered_data)
        ax[0].text(i+0.032*fontsize, stats[2]+0.45*fontsize, "max: {:.2f}".format(stats[2]), horizontalalignment='center', color='red', fontsize=fontsize)
        ax[0].text(i+0.032*fontsize, stats[0]+0.75*fontsize, "median: {:.2f}".format(stats[0]), horizontalalignment='center', color='green', fontsize=fontsize)
        ax[0].text(i+0.032*fontsize, stats[1]+0.75*fontsize, "mean: {:.2f}".format(stats[1]), horizontalalignment='center', color='orange', fontsize=fontsize )
        ax[0].text(i+0.032*fontsize, stats[3]-0.80*fontsize, "min: {:.2f}".format(stats[3]), horizontalalignment='center', color='blue', fontsize=fontsize)

        # Calculate the mean value for the CPU usage
        cpu_mean = filtered_data["cpu_usage_avg"].mean()
        cpu_thresholds.append(i)
        cpu_means.append(cpu_mean)

    # Add the line connecting the mean values of the CPU usage
    ax[0].plot(cpu_thresholds, cpu_means, marker='o', color='orange')

    # Set the x-axis labels
    ax[0].set_xticklabels(unique_thresholds)
    ax[0].set_xticks(range(len(unique_thresholds)))
    ax[0].set_xticklabels(["hpa_tresh: {}".format(int(x)) for x in unique_thresholds])

    # Draw the boxplots of the memory usage
    mem_thresholds = []
    mem_means = []
    for i, hpa_cpu_threshold in enumerate(unique_thresholds):
        # Filter the data for the current hpa_cpu_threshold
        filtered_data = data[data["hpa_cpu_threshold"] == hpa_cpu_threshold]

        # Draw the boxplot of the memory usage
        box = filtered_data.boxplot(column="memory_usage_avg", ax=ax[1], positions=[i], return_type="dict")
        stats = get_stats(filtered_data)
        ax[1].text(i+0.032*fontsize, stats[6]+0.012*fontsize, "max: {:.2f}".format(stats[6]), horizontalalignment='center', color='red', fontsize=fontsize)
        ax[1].text(i+0.032*fontsize, stats[4]+0.028*fontsize, "median: {:.2f}".format(stats[4]), horizontalalignment='center', color='green', fontsize=fontsize)
        ax[1].text(i+0.032*fontsize, stats[5]-0.048*fontsize, "mean: {:.2f}".format(stats[5]), horizontalalignment='center', color='orange', fontsize=fontsize)
        ax[1].text(i+0.032*fontsize, stats[7]-0.024*fontsize, "min: {:.2f}".format(stats[7]), horizontalalignment='center', color='blue', fontsize=fontsize)

        # Calculate the mean value for the memory usage
        mem_mean = filtered_data["memory_usage_avg"].mean()
        mem_thresholds.append(i)
        mem_means.append(mem_mean)

    # Add the line connecting the mean values of the memory usage
    ax[1].plot(mem_thresholds, mem_means, marker='o', color='orange')

    # Set the x-axis labels
    ax[1].set_xticklabels(unique_thresholds)
    ax[1].set_xticks(range(len(unique_thresholds)))
    ax[1].set_xticklabels(["hpa_tresh: {}".format(int(x)) for x in unique_thresholds])
    # Set the titles of the boxplots
    ax[0].set_title("CPU Usage")
    ax[1].set_title("Memory Usage")

    # Add labels to the y-axis of the boxplots
    ax[0].set_ylabel("CPU Usage (average in mCores)")
    ax[1].set_ylabel("Memory Usage (average in MB)")
    
    if args.latency:
        # Draw the boxplots of the HTTP Request API latencies
        latency_ax = ax[2] if args.latency else None
        latency_thresholds = []
        latency_means = []
        for i, hpa_cpu_threshold in enumerate(unique_thresholds):
            # Get the latency data for the current hpa_cpu_threshold
            latency_data = get_latency_data(hpa_cpu_threshold)
            
            # Draw the boxplot of the latency data
            box = latency_data.boxplot(column="Latency", ax=latency_ax, positions=[i], return_type="dict")
            # Add the statistics to the plot
            latency_stats = get_latency_stats(latency_data)
            latency_ax.text(i+0.032*fontsize, latency_stats[2]+0.75*fontsize, "max: {:.0f} ms".format(latency_stats[2]), horizontalalignment='center', color='red', fontsize=fontsize)
            latency_ax.text(i+0.032*fontsize, latency_stats[0]-0.68*fontsize, "median: {:.0f} ms".format(latency_stats[0]), horizontalalignment='center', color='green', fontsize=fontsize)
            latency_ax.text(i+0.032*fontsize, latency_stats[1]+0.68*fontsize, "mean: {:.0f} ms".format(latency_stats[1]), horizontalalignment='center', color='orange', fontsize=fontsize)
            latency_ax.text(i+0.032*fontsize, latency_stats[3]-0.98*fontsize, "min: {:.0f} ms".format(latency_stats[3]), horizontalalignment='center', color='blue', fontsize=fontsize)

            # Calculate the mean value for the latency
            latency_mean = latency_data["Latency"].mean()
            latency_thresholds.append(i)
            latency_means.append(latency_mean)

        # Add the line connecting the mean values of the latency
        latency_ax.plot(latency_thresholds, latency_means, marker='o', color='orange')

        # Set the x-axis labels
        latency_ax.set_xticklabels(unique_thresholds)
        latency_ax.set_xticks(range(len(unique_thresholds)))
        latency_ax.set_xticklabels(["hpa_tresh: {}".format(int(x)) for x in unique_thresholds])

        # Set the title and labels of the latency boxplot
        latency_ax.set_title("HTTP Request API Latency")
        latency_ax.set_ylabel("Latency (ms)")
        
        # Set the layout of the subplots
        fig.tight_layout(rect=[0, 0, 1, 0.95])

    # Save the figure as a SVG file
    plt.savefig("deployment_metrics_summary.svg")

if __name__ == "__main__":
    main()

