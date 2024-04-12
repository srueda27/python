import numpy as np  

def calculate_total_load(bridge_length, num_sections, user_function, precision, start_position= 0, end_position= None):
    # Compiling the user function for efficient evaluation
    compiled_user_function = compile(user_function, '<string>', 'eval')
    
    # Internal function to load distribution using the pre-compiled user function
    def load_distribution(x):
        return eval(compiled_user_function, {"x": x, "np": np})

    if end_position is None:
        end_position = bridge_length
        
    # Applies the composite trapezoidal rule to approximate the integral of the load distribution.
    a = start_position
    b = end_position
    n = num_sections * precision
    h = (b - a) / n
    sum = 0.5 * (load_distribution(a) + load_distribution(b))
    for i in range(1, n):
        x_i = a + i * h
        load_x_i = load_distribution(x_i)
        sum += load_x_i
    
    return h * sum

# How to use
bridge_length = 25  # Length of the bridge in meters.
num_sections = 100  # Number of sections for the calculation.
user_function = "3 * x + 2"  # User-defined load distribution function as a string.
precision = 10
start_position = 0
end_position = 15

# Calculate the total load on the bridge.
total_load = calculate_total_load(bridge_length, num_sections, user_function, precision, start_position, end_position)

print("The total load on the bridge from position 0 to 15 meters is:", total_load, "kilograms")

# Calculate the total load on the bridge.
total_load = calculate_total_load(bridge_length, num_sections, user_function, precision)

print("The total load on the bridge is:", total_load, "kilograms")