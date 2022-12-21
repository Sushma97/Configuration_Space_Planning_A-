# Configuration_Space_Planning_A*

https://courses.grainger.illinois.edu/cs440/fa2022/MPs/mp3/assignment3.html

Many animals can change their aspect ratio by extending or bunching up. This allows animals like cats and rats to fit into small places and squeeze through small holes.
You will be moving an alien robot based on this idea. Specifically, the robot lives in 2D and has three degrees of freedom:
- It can move the (x,y) position of its center of mass.
- It can switch between three forms: a long horizontal form, a round form, and a long vertical form.

Notice that the robot cannot rotate. Also, to change from the long vertical form to/from the long horizontal form, the robot must go through the round form, i.e., it cannot go from its vertical oblong shape to its horizontal oblong shape directly.

For each planning problem we will be given a 2D environment specified by:
- The size of the workspace.
- The widths of the long and round forms.
- The starting (x,y) center-of-mass position and shape of the alien.
- A list of goals, each of which is defined by disk described by an (x,y) position and a radius.
- A set of obstacles, each of which is a line segment.
We need to find the shortest path for the alien robot from its starting position to ONE of the goal positions.

To run the code:

```python3 mp3.py --map [MapName] --config maps/test_config.txt --save-maze [MazeDestinaton].txt```

## I hereby state that I shall not be held responsible for any misuse of my work or any academic integrity violations. ##
## DO NOT COPY. Only for reference ##