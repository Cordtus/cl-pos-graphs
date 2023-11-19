import pandas as pd
import matplotlib.pyplot as plt
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
    return df

def plot_liquidity_vs_ticks(df, output_path):
    # Sort the DataFrame by 'lower_tick' to create a meaningful line chart
    sorted_df = df.sort_values('lower_tick')

    # Create a logarithmic line chart
    plt.figure(figsize=(15, 10))
    plt.plot(sorted_df['lower_tick'], sorted_df['liquidity_amount'], marker='o', linestyle='-')
    plt.xlabel('Lower Tick Value')
    plt.ylabel('Liquidity Amount')
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.title('Logarithmic Line Chart of Liquidity Amounts vs. Lower Tick')
    plt.grid(True)
    plt.savefig(output_path)  # Save the plot as a PNG file
    plt.close()  # Close the plot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a logarithmic line chart from JSON data.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file containing the dataset')
    parser.add_argument('output_path', type=str, help='Path to save the output PNG file')
    args = parser.parse_args()

    data = read_data(args.file_path)
    df = preprocess_data(data)
    plot_liquidity_vs_ticks(df, args.output_path)
