import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

url = "https://lcd.osmosis.zone"
query_path = "/osmosis/concentratedliquidity/v1beta1/liquidity_per_tick_range"

def read_data_from_api(url, pool_id):
    data = requests.get(url + query_path, params={"pool_id": pool_id}).json()
    return data

def preprocess_data(data):
    df = pd.DataFrame(data['liquidity'])
    df['liquidity_amount'] = pd.to_numeric(df['liquidity_amount'])
    df['lower_tick'] = pd.to_numeric(df['lower_tick'])
    df['upper_tick'] = pd.to_numeric(df['upper_tick'])
    df['tick_range'] = df['upper_tick'] - df['lower_tick']
    return df

def plot_3d_liquidity(df, output_file):
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
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a 3D scatter plot from pool data.')
    parser.add_argument('pool_id', type=int, help='Pool ID')
    parser.add_argument('output_path', type=str, help='Path to save the output PNG file')
    args = parser.parse_args()
    data = read_data_from_api(url, args.pool_id)
    df = preprocess_data(data)
    plot_3d_liquidity(df, f"{args.output_path}/pool_{args.pool_id}_{time.strftime('%Y%m%d-%H%M%S')}.png")

