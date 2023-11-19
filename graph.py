import matplotlib.pyplot as plt
import pandas as pd
import json
import argparse

def plot_liquidity_distribution(file_path, plot_type, save=False):
    """
    Plots the liquidity distribution from the given JSON dataset file.

    :param file_path: Path to the JSON file containing the dataset.
    :param plot_type: Type of plot - "histogram" or "line".
    :param save: Boolean, if True, saves the plot instead of displaying.
    """
    # Read data from JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data['liquidity'])
    df['liquidity_amount'] = df['liquidity_amount'].astype(float)
    df['lower_tick'] = df['lower_tick'].astype(int)
    df['upper_tick'] = df['upper_tick'].astype(int)

    # Plotting
    plt.figure(figsize=(15, 8))

    if plot_type == "histogram":
        plt.hist(df['liquidity_amount'], bins=100, color='skyblue', alpha=0.7)
        plt.xlabel('Liquidity Amount')
        plt.ylabel('Frequency')
        plt.title('Histogram of Liquidity Distribution')

    elif plot_type == "line":
        plt.plot(df['lower_tick'], df['liquidity_amount'], color='blue', marker='o', linestyle='dashed', linewidth=2, markersize=6)
        plt.xlabel('Lower Tick Value')
        plt.ylabel('Liquidity Amount')
        plt.title('Line Plot of Liquidity Amount vs. Lower Tick')

    else:
        raise ValueError("Invalid plot type. Choose 'histogram' or 'line'.")

    plt.tight_layout()
    plt.show()

    if save:
        plt.savefig(f'{file_path}_{plot_type}.png')  # Save the plot as a PNG file
    else:
        plt.show()  # Display the plot

def main():
    parser = argparse.ArgumentParser(description='Plot liquidity distribution from a JSON dataset.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file containing the dataset')
    parser.add_argument('plot_type', type=str, choices=['histogram', 'line'], help='Type of plot: histogram or line')
    parser.add_argument('--save', action='store_true', help='Save the plot instead of displaying it')

    args = parser.parse_args()

    plot_liquidity_distribution(args.file_path, args.plot_type, args.save)

if __name__ == "__main__":
    main()
