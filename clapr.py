import requests

# Constants
SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60

# Base URLs
pool_details_url = "https://lcd.osmosis.zone/osmosis/concentratedliquidity/v1beta1/pool"
spot_price_url = "https://lcd.osmosis.zone/osmosis/poolmanager/v2/spot_price_v2"
claimable_spread_rewards_url = "https://lcd.osmosis.zone/osmosis/concentratedliquidity/v1beta1/claimable_spread_rewards"
claimable_incentives_url = "https://lcd.osmosis.zone/osmosis/concentratedliquidity/v1beta1/claimable_incentives"
position_by_id_url = "https://lcd.osmosis.zone/osmosis/concentratedliquidity/v1beta1/position_by_id"

# Functions to retrieve data
def get_pool_details(pool_id):
    response = requests.get(f"{pool_details_url}/{pool_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve pool details.")
        return None

def get_spot_price(pool_id, token0_denom, token1_denom):
    params = {
        "pool_id": pool_id,
        "base_asset_denom": token0_denom,
        "quote_asset_denom": token1_denom
    }
    response = requests.get(spot_price_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve spot price.")
        return None

def get_incentive_records(pool_id):
    params = {"pool_id": pool_id}
    response = requests.get(incentive_records_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve incentive records.")
        return None

def get_claimable_spread_rewards(position_id):
    response = requests.get(f"{claimable_spread_rewards_url}/{position_id}")
    if response.status_code == 200:
        data = response.json()
        return data['claimable_spread_rewards']
    else:
        print("Failed to retrieve claimable spread rewards.")
        return None

def get_claimable_incentives(position_id):
    response = requests.get(f"{claimable_incentives_url}/{position_id}")
    if response.status_code == 200:
        data = response.json()
        return data['claimable_incentives']
    else:
        print("Failed to retrieve claimable incentives.")
        return None

def get_position_details(position_id):
    response = requests.get(f"{position_by_id_url}/{position_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve position details.")
        return None

def calculate_base_price(spot_price, lower_tick, upper_tick):
    # This function needs to be adjusted based on how you define 'base_price'
    # For the sake of the example, let's calculate the geometric mean of the spot price and the mid-point of the lower and upper bounds.
    midpoint_tick = (lower_tick + upper_tick) / 2
    base_price = (spot_price * midpoint_tick) ** 0.5
    return base_price

def calculate_unit_liquidity(liquidity, lower_tick, upper_tick):
    # Adjust this function based on how you define 'unit_liquidity'
    # For the example, let's use the square root formula mentioned earlier.
    lower_sqrt_price = lower_tick ** 0.5
    upper_sqrt_price = upper_tick ** 0.5
    unit_liquidity = liquidity / (upper_sqrt_price - lower_sqrt_price)
    return unit_liquidity

# Function to calculate APR
def calculate_apr(position_id, calculation_time_duration):
    position_details = get_position_details(position_id)
    if not position_details:
        return 0  # If we failed to get position details, we can't calculate APR

    pool_id = position_details['position']['pool_id']
    liquidity = float(position_details['position']['liquidity_amount'])
    lower_tick = float(position_details['position']['lower_tick'])
    upper_tick = float(position_details['position']['upper_tick'])

    # Retrieve claimable spread rewards and incentives for the position
    spread_rewards = get_claimable_spread_rewards(position_id)
    incentives = get_claimable_incentives(position_id)

    if not spread_rewards or not incentives:
        return 0  # If we failed to get rewards, we can't calculate APR

    # Calculate the unit of liquidity
    unit_liquidity = calculate_unit_liquidity(liquidity, lower_tick, upper_tick)

    # Calculate the base price using the spot price and liquidity range
    pool_details = get_pool_details(pool_id)
    if pool_details:
        token0_denom = pool_details['pool']['token0']
        token1_denom = pool_details['pool']['token1']
        spot_price_response = get_spot_price(pool_id, token0_denom, token1_denom)
        if spot_price_response:
            spot_price = float(spot_price_response['spotPrice'])
            base_price = calculate_base_price(spot_price, lower_tick, upper_tick)
        else:
            print("Failed to retrieve spot price.")
            return 0
    else:
        print("Failed to retrieve pool details.")
        return 0

    # Sum up the total spread rewards and incentive rewards
    total_spread_reward = sum(float(reward['amount']) for reward in spread_rewards)
    total_incentive_reward = sum(float(incentive['amount']) for incentive in incentives)

    # Calculate spread and incentive reward per unit liquidity
    spread_reward_per_unit = total_spread_reward / unit_liquidity
    incentive_reward_per_unit = total_incentive_reward / unit_liquidity

    # Calculate APR
    apr = ((spread_reward_per_unit + incentive_reward_per_unit) / base_price) * (SECONDS_IN_YEAR / calculation_time_duration) * 100

    # Return both the APR and the individual reward components
    return apr, spread_reward_per_unit, incentive_reward_per_unit

def main(position_id, calculation_time_duration):
    # Calculate the APR
    apr, spread_reward_per_unit, incentive_reward_per_unit = calculate_apr(position_id, calculation_time_duration)

    # Print the APR and reward components
    print(f"The APR for position {position_id} is: {apr:.2f}%")
    print(f"Spread Reward per Unit Liquidity: {spread_reward_per_unit}")
    print(f"Incentive Reward per Unit Liquidity: {incentive_reward_per_unit}")

if __name__== "__main__":
    position_id = input("Enter the position ID: ")  # User provides the position ID
    calculation_time_duration = float(input("Enter the calculation time duration in seconds: "))  # User provides the duration

    # Execute the main function with the user input
    main(position_id, calculation_time_duration)
