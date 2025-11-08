import numpy as np
import pickle


# Test coefficients one by one
TAPS = 5
SIZE = 100
seq = np.random.randint(-32 >> 2, 32 >> 2, size=SIZE)
# seq = -np.ones(SIZE, dtype=int)
# seq[SIZE//2:] = 0
h = np.ones(TAPS, dtype=int)  # Simple moving average filter coefficients
h[::2] = -1
# h = np.zeros(TAPS, dtype=int)
# h[-1] = 1
# h = np.random.randint(-32 >> TAPS, 32 >> TAPS, size=TAPS)
y = np.clip(np.convolve(seq, h, mode='full')[:SIZE], -32, 32)  # Perform convolution and truncate to SIZE


with open("test_data.pkl", "wb") as f:
    pickle.dump({"seq": seq.tolist(), "h":h.tolist(), "y":y.tolist()}, f)

print(seq.tolist())  # Convert numpy array to list for printing
print("---")
print(h.tolist())
print("---")
print(y.tolist())
