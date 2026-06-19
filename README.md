# Graph Editor

An interactive graph editor built with Python, NetworkX, and Tkinter. Create, visualize, and analyze graphs with a simple GUI.

## Requirements

- Python 3.x
- `networkx`
- `matplotlib`
- `tkinter` (usually included with Python)

Install dependencies with:

```bash
pip install networkx matplotlib
```

## Running the App

```bash
python graph_editor.py
```

## Features

### Add Nodes and Edges
- Type a node name and click **Add node** to add it to the graph.
- Enter two existing node names and click **Add edge** to connect them.

### Remove Nodes and Edges
- Enter a node name and click **Remove node** to delete it along with all its connected edges.
- Enter two node names and click **Remove edge** to remove the connection between them.

### Color Nodes
- Enter a node name and a color name, then click **Color node** to manually set a node's color.
- Supported colors include: `red`, `green`, `blue`, `yellow`, `purple`, `orange`, and many more (see the `colors` list in the source code for the full list).

### Chromatic Coloring
- Click **Chromatic coloring** to toggle automatic graph coloring using a greedy algorithm.
- Each node is assigned a color such that no two adjacent nodes share the same color.
- The **chromatic number** (minimum colors used) is displayed below the button.
- The button turns green when active and red when off.

### Euler Graph Analysis
- Click **Euler graph** to check whether the graph is:
  - An **Euler graph** (has an Eulerian circuit — every edge visited exactly once, returning to the start)
  - A **semi-Euler graph** (has an Eulerian path — every edge visited exactly once, without returning to the start)
  - Neither
- The Eulerian circuit or path is displayed if one exists.

### Walk (Shortest Path)
- Enter a start node and an end node, then click **Walk from A to B**.
- The shortest path between the two nodes is displayed.

### Random Graph
- Enter a number and click **Random graph** to generate a random graph with that many nodes and a random number of edges.
- Click **Clear graph** to reset the graph entirely.

### Import and Export
- Enter a file name (without extension) in the **File name** field.
- Click **Export graph** to save the current graph to a `.txt` file in the same directory as the script.
- Click **Import graph** to load a previously saved graph from a `.txt` file.

## File Format

Saved graph files use a simple text format, one node per line:

```
node_name: color: neighbor1 neighbor2 neighbor3
```

Example:

```
1: gray: 2 3
2: gray: 1 3
3: gray: 1 2
```

## Notes

- The graph is **undirected** — edges go both ways.
- If the graph is planar, it is drawn using a planar layout; otherwise a standard layout is used.
- Chromatic coloring overrides any manually set node colors while active.
