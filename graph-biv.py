import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import argparse

def plot_liquidity_vs_ticks(file_path, save=False):
    # Read data from JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data['liquidity'])
    df['liquidity_amount'] = pd.to_numeric(df['liquidity_amount'])
    df['lower_tick'] = pd.to_numeric(df['lower_tick'])

    plt.figure(figsize=(15, 8))

    # Generate a hexbin plot with a logarithmic scale on liquidity
    plt.hexbin(df['lower_tick'], df['liquidity_amount'], gridsize=50, cmap='Blues', bins='log')
    plt.colorbar(label='log10(density)')
    plt.xlabel('Lower Tick Value')
    plt.ylabel('Liquidity Amount (log scale)')
    plt.yscale('log')
    plt.title('2D Histogram of Liquidity Amount vs. Lower Tick')

    if save:
        plt.savefig(f'{file_path}_hexbin.png')  # Save the plot as a PNG file
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='2D Histogram of Liquidity vs. Ticks from a JSON dataset.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file containing the dataset')
    parser.add_argument('--save', action='store_true', help='Save the plot instead of displaying it')

    args = parser.parse_args()

    plot_liquidity_vs_ticks(args.file_path, args.save)

if __name__ == "__main__":
    main()
