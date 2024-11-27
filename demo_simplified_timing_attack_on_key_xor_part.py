import time
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Simulate AES key and plaintexts
np.random.seed(42)  # For reproducibility
key = np.random.randint(0, 256, size=16)  # 16-byte AES key
plaintexts = np.random.randint(0, 256, size=(1000, 16))  # 1000 random plaintexts

# Simulated timing function
def simulated_aes_timing(key_byte, plaintext_byte):
    # Simulate some timing variation based on XOR of key and plaintext byte
    xor_result = key_byte ^ plaintext_byte
    base_time = 0.1  # Base time in microseconds
    variable_time = (xor_result % 10) * 0.01  # Simulated variable time component
    return base_time + variable_time

# Measure timings
timings = defaultdict(list)
for plaintext in plaintexts:
    plaintext_byte = plaintext[13]  # Targeting the 14th byte (index 13)
    start_time = time.time()
    _ = simulated_aes_timing(key[13], plaintext_byte)
    end_time = time.time()
    timings[plaintext_byte].append(end_time - start_time)

# Analyze timings to deduce the key byte
average_timings = {byte: np.mean(times) for byte, times in timings.items()}
max_timing_byte = max(average_timings, key=average_timings.get)

# Known key timing analysis (simulated)
known_key_timings = {byte: simulated_aes_timing(8, byte) for byte in range(256)}
max_known_timing_byte = max(known_key_timings, key=known_key_timings.get)

# Deduce the key byte
deduced_key_byte = max_timing_byte ^ max_known_timing_byte
actual_key_byte = key[13]

print(f"Deduced key byte: {deduced_key_byte}")
print(f"Actual key byte: {actual_key_byte}")

# Plotting for visualization
plt.figure(figsize=(12, 6))
#plt.plot(average_timings.keys(), average_timings.values(), 'o-', label='Measured Timings')
plt.plot(average_timings.keys(), average_timings.values(), 'o', label='Measured Timings')
plt.axvline(x=max_timing_byte, color='r', linestyle='--', label='Max Timing Byte')
plt.xlabel('Plaintext Byte Value')
plt.ylabel('Average Timing (s)')
plt.title('Timing Attack Analysis on XOR Operation')
plt.legend()
plt.grid(True)
plt.show()

"""
Sample out:
Deduced key byte: 162
Actual key byte: 202
"""