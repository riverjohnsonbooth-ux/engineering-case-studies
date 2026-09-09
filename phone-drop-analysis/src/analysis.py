import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# List of CSV files containing acceleration data from multiple drop tests
files = [
    '2phonedrop.csv',
    '1phonedrop.csv',
    '3phonedrop.csv',
    '4phonedrop.csv',
    '5phonedrop.csv'
]

includedData = 400  # Number of samples to include before and after the peak
A_all = []          # Stores acceleration arrays for averaging
t_all = []          # Stores time arrays
first = True        # Used to label only the first individual plot line


def process_drop(file, includedData):
    """
    Loads a single drop test file, identifies the main impact peak,
    extracts a fixed window around the peak, and shifts time so that
    the peak occurs at t = 0.
    """
    phonedata = np.loadtxt(file, skiprows=2, delimiter=',')
    t = phonedata[:, 0]      # Time (s)
    A = phonedata[:, 4]      # Total acceleration (g)

    # Identify peaks with sufficient prominence to isolate the impact based on noise level
    peaks, _ = find_peaks(A, prominence=3)
    peak_index = peaks[np.argmax(A[peaks])]  # Index of the largest peak

    # Extract a symmetric window around the peak
    start = peak_index - includedData
    end = peak_index + includedData

    # (Note: Data outside this window is flat baseline, so trimming does not remove useful information)
    t_cut = t[start:end]
    A_cut = A[start:end]

    # Shift time so that the impact peak occurs at t = 0
    t_shifted = t_cut - t[peak_index]

    return t_shifted, A_cut


# Process each file and plot individual traces
for file in files:
    t_shifted, A_cut = process_drop(file, includedData)
    A_all.append(A_cut)
    t_all.append(t_shifted)

    if first:
        plt.plot(t_shifted, A_cut, 'mediumpurple', linewidth=1,
                 label='Individual drops', alpha=0.3)
        first = False
    else:
        plt.plot(t_shifted, A_cut, 'mediumpurple', linewidth=1, alpha=0.3)

# Convert list of arrays into a 2D array for averaging
A_all = np.array(A_all)

# Compute mean acceleration at each time point across all tests
A_mean = np.mean(A_all, axis=0)

# Plot mean trace
plt.plot(t_shifted, A_mean, 'blueviolet', linewidth=1, label='Mean')

# Identify peaks in the final processed dataset (for visual confirmation)
peaks, _ = find_peaks(A_cut, prominence=3)
plt.plot(t_shifted[peaks], A_cut[peaks], "x", label="Detected peaks")

plt.xlabel('Time relative to peak (s)')
plt.ylabel('Acceleration (g)')
plt.title('Phone Drop Experiments')
plt.grid(True)
plt.legend()
plt.show()


plt.figure()
colours = ['yellow', 'orange', 'red', 'deeppink', 'magenta']

for i, A_cut in enumerate(A_all):
    t_shifted = t_all[i]
    plt.plot(t_shifted, A_cut,
             color=colours[i % len(colours)],   # cycle through colours
             linewidth=1, alpha=0.8, label=f'Drop {i+1}')


plt.xlabel('Time relative to peak (s)')
plt.ylabel('Acceleration (g)')
plt.title('Phone Drop Experiments – Individual Drops Only')
plt.grid(True)
plt.legend()
plt.show()

# Select a time window around the drop to inspect behaviour
mask = (t_all[0] >= -0.5) & (t_all[0] <= 0)
t_window = t_all[0][mask]
A_window = A_mean[mask]
table = np.column_stack((t_window, A_window))

t = t_all[0]
A = A_mean

g_gunits = 1.0  # Acceleration due to gravity (g)

# Estimate sensor offset by measuring acceleration during free fall
freefall_mask = (t >= -0.30) & (t <= -0.02)
A_offset = np.mean(A_mean[freefall_mask])

print("Mean g during free fall (should be ~0 g):", np.mean(A_mean[freefall_mask]))

# Correct sensor bias so free fall corresponds to 0 g
A_corrected = A_mean - A_offset

# Convert proper acceleration (measured by phone) to true acceleration
A_net = A_corrected - g_gunits

# Select free-fall interval based on visual inspection of mean acceleration data
mask = (t >= -0.350) & (t <= -0.072)
t_slice = t[mask]
A_slice = A_net[mask]

# Checking free-fall window is correct
if len(A_slice) == 0:
    print("Warning: free-fall window produced no data. Check time bounds.")

# Integrate to find velocity
area = np.trapz(A_slice, t_slice) 
print("area under curve =", area) 
g_ms2 = 9.81
dv = area*g_ms2 # in m/s 
impact_velocity = abs(dv)

# Calculate theoretical value estimated from measured drop height
h = 0.4 
theoretical_velocity = np.sqrt(2*h*g_ms2)

# Check if impact velocity is within allowable range of estimate, prompt to recheck if necessary
def check_velocity(impact_velocity, theoretical_velocity, tolerance=0.1):
    difference = abs(impact_velocity - theoretical_velocity)
    if difference <= tolerance:
        print("Impact velocity is within allowable range of theoretical velocity.")
    else:
        print("Impact velocity (", impact_velocity,") is outside of allowable range of theoretical velocity (", theoretical_velocity,"), data must be re-examined")

# Final velocity estimate
print(f"Impact velocity = {impact_velocity:.3f} m/s")
print(f"Theoretical velocity = {theoretical_velocity:.3f} m/s")
