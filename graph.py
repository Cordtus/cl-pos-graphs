import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import argparse

def plot_liquidity_distribution(file_path, plot_type, save=False):
    # Read data from JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data['liquidity'])
    df['liquidity_amount'] = pd.to_numeric(df['liquidity_amount'])
    
    plt.figure(figsize=(15, 8))

    if plot_type == "histogram":
        plt.hist(df['liquidity_amount'], bins=100, color='skyblue', alpha=0.7, log=True)
        plt.xlabel('Liquidity Amount')
        plt.ylabel('Frequency (Log Scale)')
        plt.title('Histogram of Liquidity Distribution (Log Scale)')

    elif plot_type == "cdf":
        # Calculate the CDF values
        cdf = np.sort(df['liquidity_amount'])
        cdf_values = np.arange(1, len(cdf)+1) / len(cdf)
        plt.plot(cdf, cdf_values, marker='.', linestyle='none')
        plt.xlabel('Liquidity Amount')
        plt.ylabel('CDF')
        plt.title('Cumulative Distribution Function of Liquidity Amounts')

    else:
        raise ValueError("Invalid plot type. Choose 'histogram' or 'cdf'.")

    if save:
        plt.savefig(f'{file_path}_{plot_type}.png')  # Save the plot as a PNG file
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot liquidity distribution from a JSON dataset.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file containing the dataset')
    parser.add_argument('plot_type', type=str, choices=['histogram', 'cdf'], help='Type of plot: histogram or cdf')
    parser.add_argument('--save', action='store_true', help='Save the plot instead of displaying it')
    
    args = parser.parse_args()
    
    plot_liquidity_distribution(args.file_path, args.plot_type, args.save)

if __name__ == "__main__":
    main()
