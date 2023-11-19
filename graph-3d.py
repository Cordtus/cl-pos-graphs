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
    # Calculate tick range
    df['tick_range'] = df['upper_tick'] - df['lower_tick']
    return df

def plot_3d_liquidity(df, output_path):
    # Plotting
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Focusing on a smaller range where most data lies
    focus_df = df[(df['liquidity_amount'] < df['liquidity_amount'].quantile(0.99)) &
                  (df['tick_range'] < df['tick_range'].quantile(0.99))]

    img = ax.scatter(focus_df['lower_tick'], focus_df['upper_tick'], focus_df['liquidity_amount'],
                     c=focus_df['liquidity_amount'], cmap='viridis', marker='o', depthshade=True)

    # Labels and title
    ax.set_xlabel('Lower Tick Value')
    ax.set_ylabel('Upper Tick Value')
    ax.set_zlabel('Liquidity Amount')
    ax.set_title('3D Plot of Liquidity Amount vs. Tick Range')

    # Color bar
    fig.colorbar(img, ax=ax, label='Liquidity Amount')

    # Save plot to file
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a 3D scatter plot from JSON data.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file containing the dataset')
    parser.add_argument('output_path', type=str, help='Path to save the output PNG file')
    args = parser.parse_args()

    data = read_data(args.file_path)
    df = preprocess_data(data)
    plot_3d_liquidity(df, args.output_path)
