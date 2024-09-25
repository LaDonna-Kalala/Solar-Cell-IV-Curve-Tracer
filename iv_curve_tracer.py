import pyvisa
import numpy as np
import matplotlib.pyplot as plt

# Connect to the Keithley 2601B
rm = pyvisa.ResourceManager()
sourcemeter = rm.open_resource('GPIB0::26::INSTR')  # Adjust address as needed

# Define voltage sweep parameters
start_voltage = 0  # Starting voltage for the sweep
stop_voltage = 1  # Ending voltage for the sweep (adjust based on solar cell characteristics)
steps = 100  # Number of points in the sweep
voltages = np.linspace(start_voltage, stop_voltage, steps)

# Prepare arrays to store data
currents = []
powers = []

# Initialize the instrument
sourcemeter.write("*RST")  # Reset the sourcemeter to default settings
sourcemeter.write(":SOUR:FUNC VOLT")  # Set to voltage source mode
sourcemeter.write(":SENS:FUNC 'CURR'")  # Measure current
sourcemeter.write(":OUTP ON")  # Turn on the output

try:
    for v in voltages:
        sourcemeter.write(f":SOUR:VOLT {v}")  # Set the source voltage
        current = float(sourcemeter.query(":READ?"))  # Measure current
        currents.append(current)
        
        power = v * current  # Calculate power
        powers.append(power)

        print(f"Voltage: {v:.3f} V, Current: {current:.6e} A, Power: {power:.6e} W")

finally:
    sourcemeter.write(":OUTP OFF")  # Turn off output after the sweep
    sourcemeter.close()

# Plot the I-V curve
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(voltages, currents, label="Current (A)")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("Solar Cell I-V Curve")
plt.grid(True)

# Plot the Power curve
plt.subplot(2, 1, 2)
plt.plot(voltages, powers, label="Power (W)", color='red')
plt.xlabel("Voltage (V)")
plt.ylabel("Power (W)")
plt.title("Solar Cell Power Output")
plt.grid(True)

plt.tight_layout()
plt.show()
