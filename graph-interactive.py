import subprocess
import sys

def install_dependencies(requirements_path='requirements.txt'):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("All dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Ensure you have the necessary permissions.")

# Call the function at the start of your script execution
install_dependencies()

import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import argparse

# Constants
default_url = "https://rest-osmosis.ecostake.com:443"
query_path = "/osmosis/concentratedliquidity/v1beta1/liquidity_per_tick_range"

# Function Definitions
def read_data_from_api(url, pool_id, block_height=None):
    headers = {"Content-Type": "application/json"}
    if block_height is not None:
        headers['x-cosmos-block-height'] = str(block_height)
    response = requests.get(url + query_path, params={"pool_id": pool_id}, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Error fetching data: HTTP status {response.status_code}")
    data = response.json()
    return data

def preprocess_data(data):
    df = pd.DataFrame(data['liquidity'])
    df['liquidity_amount'] = pd.to_numeric(df['liquidity_amount'])
    df['lower_tick'] = pd.to_numeric(df['lower_tick'])
    df['upper_tick'] = pd.to_numeric(df['upper_tick'])
    df['tick_range'] = df['upper_tick'] - df['lower_tick']
    return df

def export_to_csv(df, output_path, pool_id):
    csv_file_path = f"{output_path}/pool_{pool_id}_{time.strftime('%Y%m%d-%H%M%S')}.csv"
    df.to_csv(csv_file_path, index=False)
    print(f"Data exported to CSV file at {csv_file_path}")

def plot_3d_liquidity(df, output_file, dot_size, block_height):
    fig = plt.figure(figsize=(14, 8))  # Slightly larger to accommodate the table
    ax = fig.add_subplot(111, projection='3d')

    # Customize the title to include block height
    title = f'Liquidity Amount Per Tick Range\nHeight: {block_height}'
    ax.set_title(title)

    # Plot the 3D scatter
    focus_df = df[(df['liquidity_amount'] < df['liquidity_amount'].quantile(0.99)) &
                  (df['tick_range'] < df['tick_range'].quantile(0.99))]
    img = ax.scatter(focus_df['lower_tick'], focus_df['upper_tick'], focus_df['liquidity_amount'],
                     c=focus_df['liquidity_amount'], cmap='viridis', marker='o', s=dot_size, depthshade=True)
    ax.set_xlabel('Lower Tick Value')
    ax.set_ylabel('Upper Tick Value')
    ax.set_zlabel('Liquidity Amount')

    # Add a color bar for the scatter plot
    fig.colorbar(img, ax=ax, label='Liquidity Amount')

    # Creating an inset axes for the additional details table
    table_ax = fig.add_axes([0.05, 0.5, 0.2, 0.15])  # Adjust as needed for placement and size of the table
    table_ax.axis('tight')
    table_ax.axis('off')

    # Prepare the data for the table
    table_data = [
        ['Mean', df['liquidity_amount'].mean()],
        ['Median', df['liquidity_amount'].median()],
        ['Std Dev', df['liquidity_amount'].std()],
        ['Total Count', df['liquidity_amount'].count()]
    ]

    # Create the table and plot it
    table = table_ax.table(
        cellText=table_data,
        colLabels=['Metric', 'Value'],
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    # Save the plot to a file
    plt.savefig(output_file)
    plt.close()


# Main Execution Block
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 3D scatter plot and/or CSV from pool data.")
    parser.add_argument('--pool_id', type=str, help='Pool ID (optional, for interactive mode leave blank)')
    parser.add_argument('--block_height', type=str, help='Block height (optional, press Enter to skip)')
    parser.add_argument('--csv', choices=['yes', 'no', 'exclusively'], help='Output a CSV file in addition to the plot')
    parser.add_argument('--dot_size', type=int, default=50, help='Size of the dots in the plot, ranging from 1 to 100. Default is 50')
    parser.add_argument('--url', type=str, default=default_url, help='Node REST URL')

    args = parser.parse_args()

    # Check if Pool ID is provided, else switch to interactive mode
    if args.pool_id is None:
        args.pool_id = input("Enter the Pool ID: ")
    
    # Process data
    try:
        data = read_data_from_api(args.url, args.pool_id, args.block_height)
        df = preprocess_data(data)
        
        # Interactive mode for missing arguments
        if args.block_height is None:
            args.block_height = input("Enter the Block Height (optional, press Enter to skip): ")
        if args.csv is None:
            args.csv = input("Output a CSV file in addition to the plot? (yes/no/exclusively): ").lower()
        if args.dot_size is None:
            args.dot_size = int(input("Enter the size of the dots in the plot, ranging from 1 to 100 (default is 50): "))
        
        output_path = './data'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_file_base = f"pool_{args.pool_id}_{time.strftime('%Y%m%d-%H%M%S')}"
        if args.csv in ['yes', 'exclusively']:
            export_to_csv(df, output_path, args.pool_id)

        if args.csv != 'exclusively':
            output_file_name = f"{output_file_base}.png"
            output_file_path = os.path.join(output_path, output_file_name)
            plot_3d_liquidity(df, output_file_path, args.dot_size, args.block_height)  # Include block height here
            print(f"Plot saved to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
