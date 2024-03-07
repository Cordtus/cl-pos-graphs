import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

url = "https://osmosis-api.lavenderfive.com:443"
query_path = "/osmosis/concentratedliquidity/v1beta1/liquidity_per_tick_range"

def read_data_from_api(url, pool_id, block_height=None):
    headers = {}
    if block_height is not None:
        headers['Block-Height'] = str(block_height)
    data = requests.get(url + query_path, params={"pool_id": pool_id}, headers=headers).json()
    return data

def preprocess_data(data):
    df = pd.DataFrame(data['liquidity'])
    df['liquidity_amount'] = pd.to_numeric(df['liquidity_amount'])
    df['lower_tick'] = pd.to_numeric(df['lower_tick'])
    df['upper_tick'] = pd.to_numeric(df['upper_tick'])
    df['tick_range'] = df['upper_tick'] - df['lower_tick']
    return df

def plot_3d_liquidity(df, output_file):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    focus_df = df[(df['liquidity_amount'] < df['liquidity_amount'].quantile(0.99)) &
                  (df['tick_range'] < df['tick_range'].quantile(0.99))]
    img = ax.scatter(focus_df['lower_tick'], focus_df['upper_tick'], focus_df['liquidity_amount'],
                     c=focus_df['liquidity_amount'], cmap='viridis', marker='o', depthshade=True)
    ax.set_xlabel('Lower Tick Value')
    ax.set_ylabel('Upper Tick Value')
    ax.set_zlabel('Liquidity Amount')
    ax.set_title('3D Plot of Liquidity Amount vs. Tick Range')
    fig.colorbar(img, ax=ax, label='Liquidity Amount')
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    pool_id = input("Enter the pool ID: ")
    block_height = input("Enter the block height (optional, press Enter to skip): ")
    output_path = input("Enter the directory path to save the output file: ")
    # Verify input or set defaults if necessary
    block_height = None if block_height == '' else block_height
    try:
        data = read_data_from_api(url, pool_id, block_height)
        df = preprocess_data(data)
        output_file_name = f"pool_{pool_id}_{time.strftime('%Y%m%d-%H%M%S')}.png"
        output_file_path = f"{output_path}/{output_file_name}"
        plot_3d_liquidity(df, output_file_path)
        print(f"Plot saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
