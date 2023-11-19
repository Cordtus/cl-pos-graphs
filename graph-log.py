import pandas as pd
import matplotlib.pyplot as plt

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

def plot_liquidity_vs_ticks(df):
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
    plt.show()

if __name__ == "__main__":
    file_path = 'path_to_your_file.json'  # Replace with the actual path to your JSON file
    data = read_data(file_path)
    df = preprocess_data(data)
    plot_liquidity_vs_ticks(df)
