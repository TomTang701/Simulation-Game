import matplotlib.pyplot as plt
import os

# Data for different power generation methods
power_methods = {
    "Coal": {"efficiency": 33, "emissions": 820},
    "Natural Gas": {"efficiency": 55, "emissions": 490},
    "Nuclear": {"efficiency": 35, "emissions": 15},
    "Solar": {"efficiency": 18, "emissions": 35},
    "Wind": {"efficiency": 38, "emissions": 11},
    "Hydro": {"efficiency": 90, "emissions": 4},
    "No Power Generation": {"efficiency": 0, "emissions": -20}  # Plants absorb CO2
}

# Initialize game variables
water_supply = 1000  # in liters
population = 100
carbon_emissions = 0  # in grams
days_survived = 0
min_daily_water_per_person = 2  # in liters
carbon_emission_limit = 10000  # Carbon emission limit in grams

# Lists to store data for plotting
days = []
emissions_per_day = []
water_supply_list = []
population_list = []


# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Function to display the current status
def display_status():
    print(f"Day: {days_survived}")
    print(f"Water Supply: {water_supply} liters")
    print(f"Population: {population} (Need {population*2} Water every day)")
    print(f"Carbon Emissions: {carbon_emissions} grams")
    print(f"Carbon Emission Limit: {carbon_emission_limit} grams\n")


# Function to choose a power generation method
def choose_power_method():
    print("Choose a power generation method:")
    for i, method in enumerate(power_methods):
        water_needed = power_methods[method]['efficiency'] * 10
        carbon_emissions_method = power_methods[method]['emissions']

        # Determine water safety
        if water_supply + water_needed < population * min_daily_water_per_person:
            if water_supply + water_needed <= 0:
                water_safety = "\033[31mUnsafe (All people might die)\033[0m"  # Red
            else:
                water_safety = "\033[33mUnsafe (Some people might die)\033[0m"  # Yellow
        else:
            water_safety = "\033[32mSafe\033[0m"  # Green

        # Determine carbon safety
        total_carbon_emissions = carbon_emissions + carbon_emissions_method
        if total_carbon_emissions > carbon_emission_limit:
            carbon_safety = "\033[31mUnsafe (All people might die)\033[0m"  # Red
        else:
            carbon_safety = "\033[32mSafe\033[0m"  # Green

        print(
            f"{i + 1}. {method} (Water Supply: {water_needed} liters, Carbon Emissions: {carbon_emissions_method} grams) - Water Safety: {water_safety}, Carbon Safety: {carbon_safety}")

    if days_survived % 10 == 9 :
        print("\033[31m\nThe Report will be given tomorrow!\n\033[0m") # red

    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(power_methods):
                break
            else:
                print("Invalid choice. Please enter a number corresponding to a power generation method.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return list(power_methods.keys())[choice]


# Function to update game variables based on the chosen power method
def update_game(method):
    global water_supply, population, carbon_emissions, days_survived
    efficiency = power_methods[method]["efficiency"]
    emissions = power_methods[method]["emissions"]
    filtered_water = efficiency * 10  # Arbitrary value for simulation
    water_supply += filtered_water
    carbon_emissions += emissions
    days_survived += 1

    # Calculate the minimum water required for the current population
    min_required_water = population * min_daily_water_per_person

    # If water supply is less than required, decrease population
    if water_supply < min_required_water:
        # Calculate how many people can be sustained with the available water
        sustainable_population = water_supply // min_daily_water_per_person
        # Population decrease is the difference between current and sustainable population
        population_loss = population - sustainable_population
        population -= population_loss
        min_required_water = water_supply
        print(f"Due to water shortage, {population_loss} people have died.")

    # Deduct the minimum required water from the water supply
    water_supply -= min_required_water

    # Check for carbon emission limit after applying the method
    total_carbon_emissions = carbon_emissions
    #print(total_carbon_emissions, emissions, carbon_emission_limit)
    #if method != "No Power Generation":  # No additional emissions if no power generated
    #    total_carbon_emissions += emissions

    if total_carbon_emissions > carbon_emission_limit:
        population = 0  # All people die if the carbon emission limit is exceeded
        print("The island has been submerged due to high carbon emissions. All people have died.")

    # Append data for plotting
    days.append(days_survived)
    emissions_per_day.append(carbon_emissions / days_survived)
    water_supply_list.append(water_supply)
    population_list.append(population)

    # Plot the results every 5 days
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    if days_survived % 10 == 0 :
        plot_results()
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Function to plot the results
def plot_results():
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(days, emissions_per_day, label="Carbon Emissions (grams/day)", color="red")
    plt.xlabel("Days")
    plt.ylabel("Carbon Emissions (grams/day)")
    plt.title("Carbon Emissions Over Time")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(days, water_supply_list, label="Water Supply (liters)", color="blue")
    plt.xlabel("Days")
    plt.ylabel("Water Supply (liters)")
    plt.title("Water Supply Over Time")
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(days, population_list, label="Population", color="green")
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title("Population Over Time")
    plt.legend()

    plt.tight_layout()
    plt.show()


# Main game loop
while population > 0:
    clear_screen()
    display_status()
    chosen_method = choose_power_method()
    update_game(chosen_method)

# Game over
print("Game Over")
print(f"You survived for {days_survived} days.")

# Final plot of the results
plot_results()
