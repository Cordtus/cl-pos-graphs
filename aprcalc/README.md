# auxiliary project - an attempt to calculate some useful measure of apr for cl pools


### misc. notes/snippets
```
import requests

# Constants
SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60

# Base URLs
pool_details_url = "https://osmosis-api.lavenderfive.com:443/osmosis/poolmanager/v1beta1/pools"
positions_by_wallet_url = "https://osmosis-api.lavenderfive.com:443/osmosis/concentratedliquidity/v1beta1/positions"
position_by_id_url = "https://osmosis-api.lavenderfive.com:443/osmosis/concentratedliquidity/v1beta1/position_by_id?position_id="
spot_price_url_template = "https://lcd.osmosis.zone/osmosis/poolmanager/pools/{pool_id}/prices?base_asset_denom={token0_denom}&quote_asset_denom={token1_denom}"


def get_pool_details(pool_id):
    response = requests.get(f"{pool_details_url}/{pool_id}")
    return response.json() if response.status_code == 200 else None

def positions_by_wallet(wallet_address):
    response = requests.get(f"{positions_by_wallet_url}/{wallet_address}")
    return response.json() if response.status_code == 200 else None

def get_position_details(position_id):
    response = requests.get(f"{position_by_id_url}{position_id}")
    return response.json() if response.status_code == 200 else None

def main():
    wallet_address = input("Enter your wallet address: ")
    pool_id = input("Enter the pool ID: ")
    positions_data = positions_by_wallet(wallet_address)
    if positions_data and positions_data.get('positions'):
        for position in positions_data['positions']:
            print(f"Position ID: {position['position']['position_id']}")
        position_id = input("Enter the position ID to see further details: ")
        position_details = get_position_details(position_id)
        # Assuming position details extraction and further processing is implemented here
    else:
        print("No positions found for this wallet or failed to retrieve positions.")

def get_spot_price(pool_id, token0_denom, token1_denom):
    spot_price_url = spot_price_url_template.format(pool_id=pool_id, token0_denom=token0_denom, token1_denom=token1_denom)
    response = requests.get(spot_price_url)
    return response.json() if response.status_code == 200 else None

def calculate_base_price(spot_price, lower_tick, upper_tick):
    midpoint_tick = (lower_tick + upper_tick) / 2
    base_price = (spot_price * midpoint_tick) ** 0.5  # Adjust this calculation as per actual formula
    return base_price

def calculate_unit_liquidity(liquidity, lower_tick, upper_tick):
    lower_sqrt_price = lower_tick ** 0.5
    upper_sqrt_price = upper_tick ** 0.5
    unit_liquidity = liquidity / (upper_sqrt_price - lower_sqrt_price)  # Adjust this calculation as per actual formula
    return unit_liquidity

# Assume other functions (get_pool_details, positions_by_wallet, get_position_details) are defined here

def main():
    # Placeholder for main logic
    pass

if __name__ == "__main__":
    main()
```
