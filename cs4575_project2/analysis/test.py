# Define the median values
keras_median = {"Time": 121.512, "Energy": 4910.2352, "Power": 40.4442, "EDP": 597288.5663}
torch_median = {"Time": 196.501, "Energy": 7989.4385, "Power": 40.5893, "EDP": 1569504.3747}
jax_median = {"Time": 521.436, "Energy": 15461.0326, "Power": 29.6987, "EDP": 8055534.4505}

# Function to calculate percentage increase/decrease
def percentage_change(old, new):
    return round(((new - old) / old) * 100, 2)

# Table 1: Keras vs. Torch
print("\n### Table 1: Keras vs. Torch")
print(f"Time: {percentage_change(keras_median['Time'], torch_median['Time'])}%")
print(f"Energy: {percentage_change(keras_median['Energy'], torch_median['Energy'])}%")
print(f"Power: {percentage_change(keras_median['Power'], torch_median['Power'])}%")
print(f"EDP: {percentage_change(keras_median['EDP'], torch_median['EDP'])}%")

# Table 2: Torch vs. JAX
print("\n### Table 2: Torch vs. JAX")
print(f"Time: {percentage_change(torch_median['Time'], jax_median['Time'])}%")
print(f"Energy: {percentage_change(torch_median['Energy'], jax_median['Energy'])}%")
print(f"Power: {percentage_change(torch_median['Power'], jax_median['Power'])}%")
print(f"EDP: {percentage_change(torch_median['EDP'], jax_median['EDP'])}%")

# Table 3: Keras vs. JAX
print("\n### Table 3: Keras vs. JAX")
print(f"Time: {percentage_change(keras_median['Time'], jax_median['Time'])}%")
print(f"Energy: {percentage_change(keras_median['Energy'], jax_median['Energy'])}%")
print(f"Power: {percentage_change(keras_median['Power'], jax_median['Power'])}%")
print(f"EDP: {percentage_change(keras_median['EDP'], jax_median['EDP'])}%")
