import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

def read_data(file_path):
    # Read the JSON data file
    with open(file_path, 'r') as file:
        data = pd.read_json(file)
    return data

def preprocess_data(data):
    # Convert the nested 'liquidity' data into a DataFrame
    df = pd.json_normalize(data['liquidity'])
    # Convert strings to numeric values
    df['liquidity_amount'] = pd.to_numeric(df['liquidity_amount'])
    df['lower_tick'] = pd.to_numeric(df['lower_tick'])
    df['upper_tick'] = pd.to_numeric(df['upper_tick'])
    return df

def plot_3d_liquidity(df, output_path):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')

    # 3D Scatter plot
    scatter = ax.scatter(df['lower_tick'], df['upper_tick'], df['liquidity_amount'], c=df['liquidity_amount'], cmap='viridis', marker='o')

    # Labels and title
    ax.set_xlabel('Lower Tick Value')
    ax.set_ylabel('Upper Tick Value')
    ax.set_zlabel('Liquidity Amount')
    ax.set_title('3D Plot of Liquidity Amount vs. Tick Range')

    # Colorbar for liquidity amounts
    fig.colorbar(scatter, ax=ax, label='Liquidity Amount')

    # Save the plot
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a 3D plot from JSON data.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file containing the dataset')
    parser.add_argument('output_path', type=str, help='Path to save the output PNG file')
    args = parser.parse_args()

    data = read_data(args.file_path)
    df = preprocess_data(data)
    plot_3d_liquidity(df, args.output_path)
