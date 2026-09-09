**Phone Drop Impact Analysis**
This case study investigates the acceleration profile of a smartphone during multiple drop tests. The goal is to analyse impact behaviour, identify consistent features across drops, estimate free‑fall velocity, and compare the measured impact velocity to the theoretical value based on drop height.

The project demonstrates:

-time‑series processing
-peak detection
-signal alignment
-averaging across experiments
-sensor bias correction
-numerical integration
-physics‑based validation

All code, data, and plots are included for full reproducibility.

**1. Overview**

A smartphone was dropped from a known height while recording acceleration using a built‑in sensor. Five separate drops were performed to capture variability in impact behaviour. The acceleration data was processed to identify the impact peak, align all drops in time, and compute an average acceleration trace. 
The free‑fall portion of the signal was used to estimate impact velocity, which was compared against the theoretical velocity calculated from the drop height.


**2. Data Collection**
Device: Smartphone accelerometer

Sampling rate: ~100 Hz (approx.)

Number of drops: 5

Recorded channels:
Time (s)
Acceleration (g)

Drop height: 0.40 m

Raw CSV files are stored in the data/ directory.


**3. Methodology**
  3.1 Peak Detection
  Each dataset is processed using scipy.signal.find_peaks to identify the main impact peak.
  A fixed window around the peak is extracted to isolate the relevant portion of the signal.

  3.2 Time Alignment
  Time is shifted so that the impact peak occurs at t = 0 for all drops.
  This allows direct comparison and averaging.

  3.3 Averaging
  Aligned acceleration traces are stacked and averaged to produce a mean acceleration curve representing a “typical” drop.

  3.4 Sensor Offset Correction
  Acceleration during free‑fall should be ~0 g.
  The mean value in the free‑fall window is used to estimate sensor bias, which is subtracted from the signal.

  3.5 True acceleration
  The phone measures proper acceleration so gravity must be removed:
  a_net = a_corrected - 1g

  3.6 Velocity Estimation
  Velocity is estimated by integrating net acceleration over the free-fall interval
  v = ∫ a_net(t) dt
  Converted to m/s using 9.81m/s^2

  3.7 Theoretical Velocity
Using drop height h=0.4m
v_theoretical = √(2gh)

The measured velocity is compared to the theoretical value with a tolerance of ±0.1 m/s.

**4. Results**
   4.1 Individual Drops
   All drops show similar impact profiles. A separate plot shows each drop in a unique colour

   4.2 Mean Acceleration
   The mean acceleration plot highlights consistent regions: free fall, impact peak and post impact oscillations

   4.3 Impact Velocity
   After correcting for sensor bias:
   Impact velocity = 2.811 m/s
   Theoretical velocity = 2.801 m/s

**5. Plots**
   Plots are stored in the plots/ directory

**6. Code**
   Full analysis script is found in src/analysis.py
   A Jupyter notebook containing exploratory work can be found in notebooks/Phone_drop_analysis.ipynb


