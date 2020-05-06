# Street-Specification-to-Undirected-Graph

Given a set of streets, we can represent them as an undirected graph which can be visualized to highlight the endpoints of the streets along with the intersections that occur between the streets. This repository contains a program that takes in a collection of multiple streets represented as poly-line segments and generate a graph from them by outputting a list of all the vertices and edges in that graph. Such a program could be helpful for an entity such as the Traffic Department to analyze potential location of traffic cameras.


## Getting Started

In order to run the program, firstly, you must clone the repository on your local machine. You can do this by running the following line on your machine's CLI:

```git clone https://github.com/SafiyaJan/Street-Specification-to-Undirected-Graph.git```

### Prerequisites

Ensure that you have Python3 installed on your machine in order to run program. Check out the following link to install the correction version of Python on your specific machine:
https://realpython.com/installing-python/

## Usage 

### Running the program

To run the program, type the following on your command line:
```python3 input_parser.py```

#### Adding a street
To add a street enter to the street set, enter the command in the following format:
```
a "<Street Name>" (x1,y1), (x2,y2), (x3,y3).. 
# For example:
a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)
```

#### Removing a street
To remove a street from the street set, enter the command in the following format:
```
r "<Street Name>"  
# For example:
r "Weber Street"
```
Note - A street can only be removed after being adding to the street set

#### Changing a street
To remove a street from the street set, enter the command in the following format:
```
c "<Street Name>" (x1,y1), (x2,y2), (x3,y3).. 
# For example:
c "Weber Street" (2,1) (2,2)
```
Note - A street can only be changed after being adding to the street set

#### Generating graph
To generate the graph from the street set, type ```g``` after adding multiple streets to the street set:
```
#input
a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)
a "King Street S" (4,2) (4,8)
a "Davenport Road" (1,4) (5,8)
g #generate graph

#output
V = {
1: (2,2)
2: (4,2)
3: (4,4)
4: (5,5)
5: (1,4)
6: (4,7)
7: (5,6)
8: (5,8)
9: (3,8)
10: (4,8)
}
E = {
<1,3>,
<2,3>,
<3,4>,
<3,6>,
<7,6>,
<6,5>,
<9,6>,
<6,8>,
<6,10>
}
```
Note - A graph can only be generated when there is atleast one street in the street set
