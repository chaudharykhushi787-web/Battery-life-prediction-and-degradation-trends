from google.colab import files
uploaded = files.upload()



import scipy.io as sio

data = sio.loadmat("B0005.mat")
battery = data['B0005']


cycles = battery['cycle'][0,0][0]
len(cycles)



discharge_cycles = []

for cycle in cycles:
    if cycle['type'][0] == 'discharge':
        discharge_cycles.append(cycle)
len(discharge_cycles)


example_cycle = cycles[0]
example_cycle.dtype.names      

example_cycle['type'][0]



discharge_cycles = []

for cycle in cycles:
    ctype = str(cycle['type'][0]).lower().strip()
    if ctype == "discharge":
        discharge_cycles.append(cycle)

len(discharge_cycles)


first_discharge = discharge_cycles[0]
first_discharge.dtype.names


first_discharge['data'][0][0].dtype.names


Qd = first_discharge['data'][0][0]['Capacity'][0]
Qd[-1]





capacities = []

for i, cycle in enumerate(discharge_cycles):
    # Sometimes cycle number is just the index + 1
    cycle_num = i + 1

    # Extract capacity vector
    cap_vec = cycle['data'][0][0]['Capacity'][0]

    # Store last value of capacity for this cycle
    capacities.append(cap_vec[-1])

print(capacities)

import numpy as np

capacities = np.array(capacities)
initial_capacity = capacities[0]  # first cycle capacity
SOH = capacities / initial_capacity  # normalized to 1



capacities = np.array(capacities)  # make sure it's a NumPy array
initial_capacity = capacities[0]   # capacity of first cycle
SOH = capacities / initial_capacity  # normalized SOH

print("SOH values:\n", SOH)



import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.plot(range(1, len(SOH)+1), SOH, marker='o', color='orange')
plt.xlabel('Cycle Number')
plt.ylabel('State of Health (SOH)')
plt.title('Battery SOH vs Cycle Number')
plt.grid(True)
plt.show()



SOH_threshold = 0.8  # End-of-life threshold



RUL = []

for i, soh in enumerate(SOH):
    remaining_cycles = sum(SOH[i:] > SOH_threshold)
    RUL.append(remaining_cycles)

RUL = np.array(RUL)





plt.figure(figsize=(8,5))
plt.plot(range(1, len(RUL)+1), RUL, marker='o', color='green')
plt.xlabel('Cycle Number')
plt.ylabel('RUL (Remaining Useful Life in cycles)')
plt.title('Battery RUL Prediction')
plt.grid(True)
plt.show()



import pandas as pd

# Assume SOH and RUL are numpy arrays
SOH = np.array(SOH)
RUL = np.array(RUL)

window_size = 5  # number of previous cycles to consider
X = []
y = []

for i in range(len(SOH) - window_size):
    X.append(SOH[i:i+window_size])  # take window of SOH
    y.append(RUL[i+window_size])    # RUL after that window

X = np.array(X)
y = np.array(y)

print("Feature shape:", X.shape)
print("Label shape:", y.shape)



from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)



from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Test MSE:", mse)
print("Test R2 Score:", r2)



last_window = SOH[-window_size:]  # last few cycles
predicted_RUL = model.predict([last_window])[0]
print(f"Predicted RUL for the current battery state: {predicted_RUL:.2f} cycles")


import numpy as np
from numpy import polyfit

cycles = np.arange(1, len(SOH)+1)
# Fit linear or exponential decay
coeffs = polyfit(cycles, SOH, 1)  # linear
m, b = coeffs
SOH_threshold = 0.8
predicted_EOL_cycle = (SOH_threshold - b) / m
predicted_RUL = predicted_EOL_cycle - len(SOH)

print(f"Predicted RUL: {predicted_RUL:.2f} cycles")


predicted_RUL = max(predicted_RUL, 0)
print(f"Predicted RUL: {predicted_RUL:.2f} cycles")





cycles = np.arange(1, len(SOH)+1)
m, b = np.polyfit(cycles, SOH, 1)

# Predicted SOH line
fitted_line = m*cycles + b

plt.figure(figsize=(8,5))
plt.plot(cycles, SOH, 'o', label='Measured SOH')
plt.plot(cycles, fitted_line, '-', label='Linear Fit')
plt.axhline(y=SOH_threshold, color='r', linestyle='--', label='EOL Threshold')
plt.xlabel('Cycle Number')
plt.ylabel('SOH')
plt.legend()
plt.grid(True)
plt.show()



# Polynomial fit (2nd degree)
coeffs = np.polyfit(cycles, SOH, 2)
poly_SO = np.poly1d(coeffs)

# Solve for EOL
from scipy.optimize import fsolve
EOL_cycle = fsolve(lambda x: poly_SO(x) - SOH_threshold, len(SOH))[0]
predicted_RUL = max(EOL_cycle - len(SOH), 0)
print(f"Predicted RUL (poly fit): {predicted_RUL:.2f} cycles")



import ipywidgets as widgets
from IPython.display import display


# cycles, SOH, RUL arrays are already available
cycles = np.arange(1, len(SOH)+1)

def plot_degradation(max_cycle):
    plt.figure(figsize=(8,5))
    plt.plot(cycles[:max_cycle], SOH[:max_cycle], marker='o', color='orange', label='SOH')
    plt.plot(cycles[:max_cycle], RUL[:max_cycle], marker='x', color='green', label='RUL')
    plt.xlabel('Cycle Number')
    plt.ylabel('Value')
    plt.title('Battery Cycle Degradation Trend')
    plt.legend()
    plt.grid(True)
    plt.show()

# Interactive slider
slider = widgets.IntSlider(value=len(cycles), min=1, max=len(cycles), step=1, description='Cycle')
widgets.interact(plot_degradation, max_cycle=slider)