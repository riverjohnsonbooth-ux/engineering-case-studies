**Barcelona Lap Acceleration Analysis**

1. **Overview**
  This project analyses sample data exported from MoTeC i2 of a lap of the Circuit de Barcelona-Catalunya, using MATLAB to generate a G-G diagram and classify vehicle behaviour into distinct regions:
  - Acceleration (left and right)
  - Pure Cornering (left and right)
  - Braking (left and right)
  - Pure Acceleration
  - Pure Braking

  The goal was  to produce motorsport style telemetry visualisation and quantify how much of the lap time was spent in each region. 
  The project demonstrates:
  - MATLAB data processing
  - Logical region classification
  - Scatter plot generation
  - Percentage distribution visualisation
  - Motorsport-relevant interpretation of IMU data


2. **Data**
   The data was provided by Racetrack Dynamics as part of a motorsport data analysis webinar streamed in August 2026. 
   Raw CSV file can be viewed in the data/ directory


3. **G-G Diagram**
  The diagram plots lateral acceleration on the x axis and longitudinal on the y axis. Initially it was unclear whether CAR_G_AX represented longitudinal or lateral data, however after generating the initial scatter plot, it soon became clear based on the shape of the graph. The resulting shape displays the car's grip envelope, with symmetry between left and right hand corners and stronger braking forces than acceleration.


4. **Region Classification**
  Each data point is assigned to one of 9 regions using logical masks:
  - Left Acceleration / Right Acceleration / Pure Acceleration
  - Left Braking / Right Braking / Pure Braking
  - Pure Left Cornering / Pure Right Cornering
  - Centre
  
    Thresholds of ± 0.4g (lateral) and ± 0.3g (longitudinal) define these regions. This classification allows quantitative analysis of how the car behaves across the lap.


5. **Percentage Distribution**
  Using groupcounts, each region's sample count is converted into a percentage of the total dataset. These percentages are visualised using a sorted horizontal bar chart. For ease of interpretation, colours are consistent for each region.
  
