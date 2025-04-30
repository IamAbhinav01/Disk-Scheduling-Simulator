# Disk-Scheduling-Simulator

# Project Overview
### The Disk-Scheduling-Simulator is a web-based application designed to simulate and visualize disk scheduling algorithms, focusing on optimizing disk I/O operations by minimizing seek time. The project implements both traditional disk scheduling algorithms (FCFS, SSTF) and advanced AI-based algorithms (APZS and RLDS), providing a comparative analysis of their performance. Built using Streamlit, the simulator offers an interactive interface where users can generate disk I/O requests, select algorithms, and visualize the disk head’s movement through an animated Matplotlib plot. Key features include:

### Traditional Algorithms: First Come First Serve (FCFS) and Shortest Seek Time First (SSTF).
#### AI-Based Algorithms:
## APZS (AI-Priority Zone Scheduling): Uses zones, priority, aging, and Exponential Moving Average (EMA) to predict and optimize scheduling.
### RLDS (Reinforcement Learning Disk Scheduling): Employs Q-learning to dynamically learn optimal request servicing order.
  ### Interactive UI: Users can adjust parameters (e.g., number of requests, zone size, learning rate) and control the simulation (start, stop, step).
  ### Visualization: Animated plot showing disk head movement, with metrics like total seek time, throughput, and predicted track.
  ### The project aims to demonstrate how AI can enhance disk scheduling, balancing efficiency (seek time) and fairness (preventing starvation), making it a valuable tool for understanding operating system concepts and AI applications.
# Tools Required
## Python 3.7+: The core programming language for the project.
## Streamlit: For building the web-based interface.
# ScreenShots
## Intial Page
![image](https://github.com/user-attachments/assets/ec571039-55b0-43ab-b02d-c9fafae11e48)
## Page of Selecting Algorithm
![image](https://github.com/user-attachments/assets/854398ea-0b3d-4f15-ad18-eeb346b0476f)
## Working
![image](https://github.com/user-attachments/assets/250c89fa-5384-4ae6-8a72-42cea2f42118)
![image](https://github.com/user-attachments/assets/e369edbb-612a-4e74-b142-6f6dcab75818)


# References
## Streamlit Documentation: https://docs.streamlit.io/
## Matplotlib Animation: https://matplotlib.org/stable/api/animation_api.html
##  Reinforcement Learning (Q-learning): “Reinforcement Learning: An Introduction” by Sutton and Barto.
## Operating Systems Concepts: “Operating System Concepts” by Silberschatz, Galvin, and Gagne (for disk scheduling basics).
## EMA in Prediction: General concepts from time-series forecasting literature.
