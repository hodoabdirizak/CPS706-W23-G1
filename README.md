## CPS 706 Winter 2023:  Project Installation Manual

# Routing Algorithm Visualization Tool

### Team Members
| Student Name | Student Number |
| :---: | :---: |
|Alex Huynh        |501025646
|Camillia Amin     |501071556
|Salma Farahat     |501026177
|Hodo Abdirizak    |501029458
|Julia Khong       |501031572
|Het Patel         |

### Table of Contents
<ol>
  <li>
    <a href="#about-the-project">About the Project</a>
    <ul>
      <li><a href="#overview">Overview</a></li>
    </ul>
    <ul>
      <li><a href="#technologies-used">Technologies Used</a></li>
    </ul>
    <ul>
      <li><a href="#collaborators">Collaborators</a></li>
    </ul>
  </li>
  <li>
    <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
      <li><a href="#running-the-program">Running the Program</a></li>
    </ul>
  </li>
  <li>
    <a href="#program-features">Program Features</a>
    <ul>
      <li><a href="#network-customization">Network Customization</a></li>
      <li><a href="#guided-implementation-of-centralized-algorithm">Guided Implementation of Centralized Algorithm</a></li>
      <li><a href="#guided-implementation-of-decentralized-algorithm">Guided Implementation of Decentralized Algorithm</a></li>
    </ul>
  </li>
  <li>
    <a href="#code">Code</a>
    <ul>
      <li><a href="#centralized-algorithm">Centralized Algorithm</a></li>
      <li><a href="#decentralized-algorithm">Decentralized Algorithm</a></li>
      <li><a href="#gui">GUI</a></li>
    </ul>
  </li>
</ol>


## About the Project

### Overview
This program is an education tool that visualizes the implementation of centralized and decentralized algorithms in routing. 

### Technologies Used 
We used the following Python libraries:
- Tkinter, to implement the GUI
- Pygame, to animate the Centralized and Decentralized Algorithms
- NetworkX, to create and manipulate the graphs
- Matplotlib, to depict the graphs

### Collaborators
- [Alex Huynh](https://github.com/alextuffy)
- [Camillia Amin](https://github.com/chamin19)
- [Het Patel](https://github.com/hetp4401)
- [Hodo Abdirizak](https://github.com/hodoabdirizak)
- [Julia Khong](https://github.com/P3anutz)
- [Salma Farahat](https://github.com/Salma-Farahat)

## Getting Started

### Prerequisites
This program requires Python version 3.10 or later. <br>

### Running the Program
1. Clone this repository. 
2. In terminal, cd into the root of the repository.
3. Run the following commands to install the necessary libraries: <br>
    - `pip install pygame` <br>
    - `pip install networkx` <br>
    - `pip install matplotlib` <br>
3. To execute the program, run `python gui/frames.py`

## Program Features

### Network Customization

### Guided Implementation of Centralized Algorithm

### Guided Implementation of Decentralized Algorithm

## Code 

### Centralized Algorithm
[Code in the `centralized` folder](https://github.com/hodoabdirizak/CPS706-W23-G1/tree/main/centralized)<br>
This folder contains the file [`dijkstra.py`](https://github.com/hodoabdirizak/CPS706-W23-G1/blob/main/centralized/dijkstra.py)
This file implements Dijkstra's algorithm and is used to generate the tables and shortest path for a networkx graph. 

### Decentralized Algorithm
[Code in the `decentralized` folder](https://github.com/hodoabdirizak/CPS706-W23-G1/tree/main/dentralized)<br>
This folder contains the file [`bellman_ford.py`](https://github.com/hodoabdirizak/CPS706-W23-G1/blob/main/decentralized/bellman_ford.py)
This file implements Bellman Ford's algorithm and is used to generate the distance vectors and shortest path for a networkx graph. 

### GUI
[Code in the `GUI` folder](https://github.com/hodoabdirizak/CPS706-W23-G1/tree/main/dentralized)<br>
This folder contains the following files:<br>
`frames.py`
- Contains the Main frame (the page first seen by the user upon executing the program) and Page1 frame (the page after passing input validation).
- Calls the approriate pygame based on user interaction. 
- Terminates the program when user presses the ESC button. 

`homepage.py`
- Used to validate the information entered by the user in the first frame. Returns an appropriate error message to `frames.py`

`create_graph.py`
- Given the data provided by the user in the Main frame, creates a randomized networkx graph and graph.png
- Given the data provided by the user in the Page1 frame, creates a customized networkx graph and graph.png
- The networkx graph is the foundation for all other files.

`centralized_pygame.py`
- Contains the code for the pygame that gets executed after the user selects the "Run centralized algorithm" button on the second page of the gui.
- Provides a description of Dijkstra's algorithm in routing.
- User proceeds to the first part of the animation by pressing any key.
- Each time the user presses the right arrow key, it shows the table being updated, stepping through each part of the algorithm.
- After the table has been completed, it backtracks the table to find the shortest path. 
- User proceeds to the second part of the animation by pressing any key.
- Each time the user presses the right arrow key, it shows the next node in the shortest path being visited in the graph. 
- Pygame terminates when the user presses the ESC key. 

`decentralized_pygame.py`
- Contains the code for the pygame that gets executed after the user selects the "Run decentralized algorithm" button on the second page of the gui.
- Provides a description of Bellman Ford's algorithm in routing. 
- User proceeds to the first part of the animation by pressing any key.
- Each time the user presses the right arrow key, it shows the distance vectors being updated, stepping through each part of the algorithm.
- After the table has been completed, it displays the shortest path and the final graph with the visited nodes highlighted. 
- Pygame terminates when the user presses the ESC key. 
