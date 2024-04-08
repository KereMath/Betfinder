import json
import os

# Load data from surebetresults.json in the Intermediatevalues folder
input_file_path = os.path.join("Intermediatevalues", "surebetresults.json")
with open(input_file_path) as f:
    games = json.load(f)

# Define function to calculate delta values
def calculate_deltas(A, B, C, x, y, z, M):
    deltaX = M * (B * C) / (A * B + A * C + B * C)
    deltaY = M * (A * C) / (A * B + A * C + B * C)
    deltaZ = M * (A * B) / (A * B + A * C + B * C)
    return deltaX, deltaY, deltaZ

# Define function to calculate M
def calculate_M(x, y, z):
    return 100 - x - y - z

# Iterate through each game and calculate new bet multiples
for game in games:
    A = game['Highest Home Odds']
    B = game['Highest Draw Odds']
    C = game['Highest Away Odds']
    x = game['Home Bet Multiple']
    y = game['Draw Bet Multiple']
    z = game['Away Bet Multiple']

    # Calculate M
    M = calculate_M(x, y, z)

    # Calculate deltas
    deltaX, deltaY, deltaZ = calculate_deltas(A, B, C, x, y, z, M)

    # Update bet multiples
    x += deltaX
    y += deltaY
    z += deltaZ

    # Update game data
    game['Home Bet Multiple'] = x
    game['Draw Bet Multiple'] = y
    game['Away Bet Multiple'] = z
    game['M'] = M

# Save the updated data to Multipliers.json in the Intermediatevalues folder
output_file_path = os.path.join("Intermediatevalues", "Multipliers.json")
with open(output_file_path, 'w') as f:
    json.dump(games, f, indent=4)
