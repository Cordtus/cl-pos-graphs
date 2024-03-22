import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import argparse

default_url = "https://osmosis-api.lavenderfive.com:443"
query_path = "/osmosis/concentratedliquidity/v1beta1/liquidity_per_tick_range"

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

def plot_3d_liquidity(df, output_file, dot_size):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    focus_df = df[(df['liquidity_amount'] < df['liquidity_amount'].quantile(0.99)) &
                  (df['tick_range'] < df['tick_range'].quantile(0.99))]
    img = ax.scatter(focus_df['lower_tick'], focus_df['upper_tick'], focus_df['liquidity_amount'],
                     c=focus_df['liquidity_amount'], cmap='viridis', marker='o', s=dot_size, depthshade=True)
    ax.set_xlabel('Lower Tick Value')
    ax.set_ylabel('Upper Tick Value')
    ax.set_zlabel('Liquidity Amount')
    ax.set_title('3D Plot of Liquidity Amount vs. Tick Range')
    fig.colorbar(img, ax=ax, label='Liquidity Amount')
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 3D scatter plot and/or CSV from pool data.")
    parser.add_argument('pool_id', type=str, help='Pool ID')
    parser.add_argument('--block_height', type=str, default=None, help='Block height (optional, press Enter to skip)')
    parser.add_argument('--csv', type=str, default='no', choices=['yes', 'no', 'exclusively'], help='Output a CSV file in addition to the plot')
    parser.add_argument('--dot_size', type=int, default=50, help='Size of the dots in the plot, ranging from 1 to 100. Default is 50')
    parser.add_argument('--url', type=str, default=default_url, help='Node REST URL')

    args = parser.parse_args()

    output_path = './data'  # Default output path
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        data = read_data_from_api(args.url, args.pool_id, args.block_height)
        df = preprocess_data(data)
        
        output_file_base = f"pool_{args.pool_id}_{time.strftime('%Y%m%d-%H%M%S')}"
        if args.csv == 'yes' or args.csv == 'exclusively':
            export_to_csv(df, output_path, args.pool_id)

        if args.csv != 'exclusively':
            output_file_name = f"{output_file_base}.png"
            output_file_path = os.path.join(output_path, output_file_name)
            plot_3d_liquidity(df, output_file_path, args.dot_size)
            print(f"Plot saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
