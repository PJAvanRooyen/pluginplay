# pluginplay
a python kivy node editor where nodes automatically take on the functionality of their given scripts

# installation
add the requirements.txt libraries to your python interpreter.

# details
In this application, you can add "node" elements that take the behavour of the scripts added to the "scripts" folder.

New scripts can be added to the folder during runtime, and they will become available for use immediately.

Nodes can be connected together to propagate results from one node to the input of the next node.

# usage
When the application runs, it will show a black screen.
## adding new functions
NOTE: currently it is limited such that the python file must:
- contain a single class
- the data-types of the paramaters and the return value of the methods in the class must be well defined.
### option 1:
Drag and drop a python file (.py) into the window. 
This will create a new node in the window and configure it with the script that was dragged in.
### option 2:
Paste any python file (.py) into the "scripts" folder. This can be done while the program is running.
See "creating nodes" and "configuring a node" for details on how to use the newly added script.
## creating nodes:
Left click anywhere on the screen to add a generic "node" element.
generic node elements do not yet have any functionality.
## configuring a node:
Double left-click on a node to choose which scrip it should take the behaviour of. 
You will be presented with a dropdown list of all the available scripts.
Some example scripts have already been provided.
Click on one of the options to configure the node.
## node usage:
Once a node is configured:
- it's left hand side will show all the input parameters of the function/method in it's script (if it has parameters).
- it's right hand side will show the return value of the function/method in it's script (if it has a return).
- left clicking on a configured node will execute it's function/method.
## node interaction:
- left click and drag from one node's output interface to another node's input interface to create a connection between nodes.
- once connected, if a node is executed, it's result will be shown on it's output interface, and that result will propagate to the input interfaces of the nodes connected to that output interface.

## example
### setup
- left click to add a node, then double left click on that node and select "incrementer".
- left click somewhere else to add another node, then double left click on that node and select "incrementer".
- connect the "float" output of the first incrementer to the "value" input of the second incrementer.
### execution
- left click on the first incrementer to execute it. 
It's input will start at 0, so after execution the output interface will show the value "1" since the input was incremented by 1.
The result will be propagated to the input of the second incrementer.
- left click on the second incrementer to execute it.
It's input value is 1 due to the execution of the first node, therefore the second incrementer shows a value of 2 on it's output after it has been executed.

