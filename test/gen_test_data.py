import numpy as np


# Test coefficients one by one
TAPS = 3
SIZE = 100
seq = np.random.randint(-32 >> TAPS, 32 >> TAPS, size=SIZE)
# seq = -np.ones(SIZE, dtype=int)
# seq[SIZE//2:] = 0
# h = np.ones(TAPS, dtype=int)  # Simple moving average filter coefficients
h = np.zeros(TAPS, dtype=int)
h[-1] = 1
h = np.random.randint(-32 >> TAPS, 32 >> TAPS, size=TAPS)
y = np.clip(np.convolve(seq, h, mode='full')[:SIZE], -32, 32)  # Perform convolution and truncate to SIZE


print(seq)
print("---")
print(h)
print("---")
print(y)
