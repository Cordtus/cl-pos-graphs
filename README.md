
# Concentrated Liquidity Positions, Graphed

---

Fully interactive [in terminal]. Generates a 3D plot chart showing the general spread, depth, and concentration of liquidity positions by calling `liquidity_per_tick_range`.

Option to export chart image (`png` format) and/or `CSV` file to `./data/` in the same directory the script is run from.

Optional block height [leave blank for default - latest height]. 

If you have issues like HTTP errors, try changing the node the script uses. There is a REST/LCD URL at the top of the script you can change for another endpoint. See [https://cosmos.directory/osmosis/nodes] for other public nodes.

```
# Constants
default_url = "https://rest-osmosis.ecostake.com:443"
```

### Features

- **Interactive Prompts**: The script prompts for necessary inputs if not provided as command-line arguments.
- **Optional Block Height**: You can specify a block height, a range of heights, a list of individual heights, or leave it blank to fetch the latest data.
- **CSV and PNG Output**: Choose to output a CSV file, a PNG file, or both.
- **Data Preprocessing**: Processes and prepares the liquidity data for visualization and export.
- **3D Plot Generation**: Generates a 3D scatter plot visualizing the liquidity distribution.

### Variables and Inputs

- **Pool ID (`--pool_id`)**: The ID of the pool for which to fetch liquidity data.
- **Heights (`--heights`)**: Specify block heights in the following formats:
  - **Single Height**: `--heights 1000`
  - **Range of Heights**: `--heights 1000-1200`
  - **List of Heights**: `--heights 1000,1005,1249`
  - **Leave blank for the latest data**.
- **CSV Option (`--csv`)**: Choose whether to output a CSV file.
  - Options: `yes`, `no`, `exclusively`
- **Dot Size (`--dot_size`)**: Size of the dots in the plot (default is 30). Range: `1-100`.
- **Node REST URL (`--url`)**: URL of the node to fetch data from (default is `https://rest-osmosis.ecostake.com:443`).

### Setup

#### Install Dependencies

Requires python/python3 + pip/pip3.

##### Install Python Packages
```sh
pip3 install -r requirements.txt
```

### Running the Script

You can run the script directly from the terminal. If you do not provide necessary inputs as command-line arguments, the script will prompt you to enter them interactively.

Example command:
```sh
python3 graph-interactive.py --pool_id 1580 --heights 1000-1100 --csv yes --dot_size 50 --url https://rest-osmosis.ecostake.com:443
```

### Troubleshooting

If you encounter HTTP errors, try changing the node endpoint in the script. Check [https://cosmos.directory/osmosis/nodes] for other public nodes.

---
