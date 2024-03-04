import requests

# Constants
SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60

# Base URLs
pool_details_url = "https://osmosis-api.lavenderfive.com:443/osmosis/poolmanager/v1beta1/pools"
position_by_id_url = "https://osmosis-api.lavenderfive.com:443/osmosis/concentratedliquidity/v1beta1/position_by_id?position_id="
spot_price_url_template = "https://lcd.osmosis.zone/osmosis/poolmanager/pools/{pool_id}/prices?base_asset_denom={token0_denom}&quote_asset_denom={token1_denom}"

def get_position_details(position_id):
    response = requests.get(f"{position_by_id_url}{position_id}")
    return response.json() if response.status_code == 200 else None

def get_pool_details(pool_id):
    response = requests.get(f"{pool_details_url}/{pool_id}")
    return response.json() if response.status_code == 200 else None

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

def calculate_apr(position_details, calculation_time_duration):
    # Extract required details from position_details
    pool_id = position_details['position']['pool_id']
    liquidity = float(position_details['position']['liquidity'])
    lower_tick = int(position_details['position']['lower_tick'])
    upper_tick = int(position_details['position']['upper_tick'])
    token0_denom = position_details['asset0']['denom']
    token1_denom = position_details['asset1']['denom']

    # Retrieve spot price
    spot_price_response = get_spot_price(pool_id, token0_denom, token1_denom)
    if not spot_price_response:
        print("Failed to retrieve spot price.")
        return 0, 0, 0

    spot_price = float(spot_price_response['spot_price']) # Adjust key as per actual API response

    # Calculate base price and unit liquidity
    base_price = calculate_base_price(spot_price, lower_tick, upper_tick)
    unit_liquidity = calculate_unit_liquidity(liquidity, lower_tick, upper_tick)

    # Sum up the total spread rewards and incentive rewards
    total_spread_reward = sum(float(reward['amount']) for reward in spread_rewards)
    total_incentive_reward = sum(float(incentive['amount']) for incentive in incentives)

    apr = ((spread_reward_per_unit + incentive_reward_per_unit) / base_price) * (SECONDS_IN_YEAR / calculation_time_duration) * 100

    return apr, spread_reward_per_unit, incentive_reward_per_unit

def main():
    position_id = input("Enter the position ID: ")
    calculation_time_duration = float(input("Enter the calculation time duration in seconds: "))

    position_details = get_position_details(position_id)
    if not position_details:
        print(f"Failed to retrieve position details for position ID {position_id}.")
        return

    apr, spread_reward_per_unit, incentive_reward_per_unit = calculate_apr(position_details, calculation_time_duration)

    if apr == 0:
        print("APR calculation failed.")
        return

    print(f"The APR for position {position_id} is: {apr:.2f}%")
    print(f"Spread Reward per Unit Liquidity: {spread_reward_per_unit}")
    print(f"Incentive Reward per Unit Liquidity: {incentive_reward_per_unit}")

if __name__ == "__main__":
    main()
