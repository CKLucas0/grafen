import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from random import randint as rd, sample
import os


name = "the_graph"
script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, f"{name}.txt")


# Create constants
graph = nx.Graph()
colors = [
    "red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "cyan",
    "magenta", "lime", "indigo", "violet", "teal", "maroon", "navy", "olive", "coral", "salmon",
    "turquoise", "gold", "silver", "beige", "ivory", "lavender", "mint", "peach", "rose", "crimson",
    "scarlet", "amber", "jade", "ruby", "sapphire", "emerald", "chartreuse", "fuchsia", "ochre", "sienna",
    "umber", "cobalt", "aqua", "periwinkle", "lilac", "mauve", "taupe", "khaki", "tan", "cream",
    "copper", "bronze", "platinum", "charcoal", "slate", "azure", "cerulean", "vermillion", "rust", "mustard",
    "apricot", "plum", "burgundy", "wine", "blush", "champagne", "lemon", "canary", "pine", "forest",
    "hunter", "moss", "sage", "fern", "seafoam", "powder", "sky", "midnight", "denim", "steel",
    "smoke", "ash", "sand", "dune", "clay", "terracotta", "brick", "mahogany", "walnut", "chestnut",
    "flax", "wheat", "buff", "ecru", "bisque", "honeydew", "thistle", "orchid", "wisteria", "mulberry"
]
chromatic = False
g = {}


# Node functions
def chromatic_colors():

    chromatic_number = 0
    busy = True
    highest_degree = None

    for node in g:
        g[node]["color"] = "white"
    # Algorithm for chromatic numbering (greedy coloring)
    while busy:

        # Find the unlabeled node with the highest degree
        highest_degree = None
        for node in g:
            if g[node]["color"] == "white":
                if highest_degree is None or len(g[node]["neighbors"]) > len(highest_degree["neighbors"]):
                    highest_degree = g[node]

        if highest_degree is None:
            break

        # Find the first available color for the chosen node
        color_index = 0
        while True:
            for neighbor in highest_degree["neighbors"]:
                if g[neighbor]["color"] == colors[color_index]:
                    color_index += 1
                    break
            else:
                break
        # Color the node
        highest_degree["color"] = colors[color_index]
        # Update the color in the NetworkX graph as well
        node_name = None
        for n, data in g.items():
            if data is highest_degree:
                node_name = n
                break
        if node_name is not None and node_name in graph.nodes:
            graph.nodes[node_name]["color"] = colors[color_index]

        # Update the chromatic number
        chromatic_number = max(chromatic_number, color_index + 1)

        # Check if all nodes are labeled
        for node in g:
            if g[node]["color"] == "white":
                break
        else:
            busy = False

    # Update the colors in the NetworkX graph to match the colors in g
    for node in graph.nodes():
        if node in g:
            graph.nodes[node]["color"] = g[node]["color"]

    # Update the colors in the NetworkX graph to match the colors in g
    for node in graph.nodes():
        if node in g:
            graph.nodes[node]["color"] = g[node]["color"]
    plt.clf()
    if nx.is_planar(graph):
        nx.draw_planar(graph, with_labels=True, node_color=[graph.nodes[node].get("color", "gray") for node in graph.nodes()])
    else:
        nx.draw(graph, with_labels=True, node_color=[graph.nodes[node].get("color", "red") for node in graph.nodes()])
    plt.draw()
    labelC.config(text=f"Chromatic number: {chromatic_number}")


def draw():
    if not chromatic:
        plt.clf()
        if nx.is_planar(graph):
            nx.draw_planar(graph, with_labels=True, node_color=[graph.nodes[node].get("color", "gray") for node in graph.nodes()])
        else:
            nx.draw(graph, with_labels=True, node_color=[graph.nodes[node].get("color", "gray") for node in graph.nodes()])
        plt.draw()
    else:
        chromatic_colors()


def walk():
    start = entryW1.get()
    end = entryW2.get()
    if graph.has_node(start) and graph.has_node(end):
        path = nx.shortest_path(graph, source=start, target=end)
        labelW.config(text=" -> ".join(path))
    else:
        labelW.config(text="Invalid nodes")


def add_node():
    node = entryK.get()
    if node and node not in graph.nodes:
        node_name = node
        graph.add_node(node_name, color="gray")
        g.update({node_name: {"color": "gray", "neighbors": []}})
        entryK.delete(0, tk.END)
        draw()


def add_edge():
    node1 = entryB1.get()
    node2 = entryB2.get()
    if node1 in graph.nodes and node2 in graph.nodes and not graph.has_edge(node1, node2):
        entryB2.delete(0, tk.END)
        graph.add_edge(node1, node2)
        g[node1]["neighbors"].append(node2)
        g[node2]["neighbors"].append(node1)
        draw()


def close_app():
    plt.close("all")
    root.destroy()


def toggle_chromatic():
    global chromatic
    chromatic = not chromatic
    if chromatic:
        buttonC.config(bg="green")
        chromatic_colors()
    else:
        buttonC.config(bg="red")
        labelC.config(text="")


def euler_graph():
    if graph.number_of_nodes() == 0:
        labelE1.config(text="The graph is empty.")
        labelE2.config(text="")
        return
    if nx.is_eulerian(graph):
        labelE1.config(text="The graph is an Euler graph.")
        labelE2.config(text=" -> ".join([f"{u}-{v}" for u, v in nx.eulerian_circuit(graph)]))
    elif nx.has_eulerian_path(graph):
        labelE1.config(text="The graph is a semi-Euler graph.")
        labelE2.config(text=" -> ".join([f"{u}-{v}" for u, v in nx.eulerian_path(graph)]))
    else:
        labelE1.config(text="The graph is neither an Euler graph nor a semi-Euler graph.")


def clear_graph():
    graph.clear()
    g.clear()
    draw()
    labelW.config(text="")
    labelE1.config(text="")
    labelE2.config(text="")


def random_graph():
    num_nodes = entryR.get()
    if not num_nodes.isdigit():
        return
    num_nodes = int(num_nodes)
    clear_graph()
    for i in range(num_nodes):
        node_name = str(i + 1)
        graph.add_node(node_name, color="gray")
        g.update({node_name: {"color": "white", "neighbors": []}})
    for i in range(num_nodes * rd(2, 4)):
        node1 = str(rd(1, num_nodes))
        node2 = str(rd(1, num_nodes))
        if node1 != node2 and not graph.has_edge(node1, node2):
            graph.add_edge(node1, node2)
            g[node1]["neighbors"].append(node2)
            g[node2]["neighbors"].append(node1)
    draw()


def read_graph():
    global g, filepath, name, script_dir
    g = {}
    with open(filepath, "r") as f:
        for line in f:
            parts = line.split(":")
            if len(parts) < 2:
                continue
            node = parts[0].strip()
            color = parts[1].strip()
            neighbors = parts[2].split() if len(parts) > 1 else []
            g[node] = {"color": color, "neighbors": neighbors}


def save_graph():
    global filepath, name, script_dir
    name = entryN.get()
    if not name:
        labelIE.config(text="Enter a file name.")
        return
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, f"{name}.txt")

    with open(filepath, "w") as f:
        for node, data in g.items():
            line = f"{node}: {data['color']}: {' '.join(data['neighbors'])}\n"
            f.write(line)


def button_read_graph():
    global filepath, name, script_dir
    name = entryN.get()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, f"{name}.txt")

    if os.path.exists(filepath):
        clear_graph()
        read_graph()
        for node, data in g.items():
            for neighbor in data["neighbors"]:
                if neighbor in g and not graph.has_edge(node, neighbor):
                    graph.add_edge(node, neighbor)
        for node in g:
            graph.add_node(node, color=g[node]["color"])
        draw()
        labelIE.config(text="")
    else:
        labelIE.config(text="File not found.")


def remove_node():
    node = entryRK.get()
    if node in g:
        for neighbor in g[node]["neighbors"]:
            g[neighbor]["neighbors"].remove(node)
            if graph.has_edge(node, neighbor):
                graph.remove_edge(node, neighbor)
        del g[node]
        graph.remove_node(node)
        draw()
        entryRK.delete(0, tk.END)


def remove_edge():
    node1 = entryRB1.get()
    node2 = entryRB2.get()
    if node1 in g[node2]["neighbors"] and node2 in g[node1]["neighbors"]:
        g[node1]["neighbors"].remove(node2)
        g[node2]["neighbors"].remove(node1)
        graph.remove_edge(node1, node2)
        draw()
        entryRB1.delete(0, tk.END)
        entryRB2.delete(0, tk.END)


def color_node():
    node = entryCKK.get()
    color = entryCKC.get()
    if node in g and color in colors:
        g[node]["color"] = color
        if node in graph.nodes:
            graph.nodes[node]["color"] = color
        draw()
        entryCKK.delete(0, tk.END)


# tkinter GUI setup
root = tk.Tk()
root.title("Graph Editor")
root.geometry("800x600")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
righter_frame = tk.Frame(root)
righter_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frameKB = tk.Frame(left_frame, bd=2, relief=tk.SUNKEN, height=200, width=300)
frameKB.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

frameRC = tk.Frame(left_frame, bd=2, relief=tk.SUNKEN, height=200, width=300)
frameRC.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frameE = tk.Frame(righter_frame, bd=2, relief=tk.SUNKEN, height=80, width=300)
frameE.pack(side=tk.TOP, fill=tk.X, expand=False)

frameR = tk.Frame(right_frame, bd=2, relief=tk.SUNKEN, height=120, width=300)
frameR.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

frameW = tk.Frame(right_frame, bd=2, relief=tk.SUNKEN, height=200, width=300)
frameW.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frameIE = tk.Frame(righter_frame, bd=2, relief=tk.SUNKEN, height=600, width=200)
frameIE.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

labelKBT = tk.Label(frameKB, text="Add Nodes and Edges", font=("Arial", 14))
labelKBT.grid(row=0, column=0, columnspan=3, pady=10)

labelKBV = tk.Label(frameKB, text="Remove Nodes and Edges", font=("Arial", 14))
labelKBV.grid(row=3, column=0, columnspan=3, pady=10)

labelKBC = tk.Label(frameKB, text="Color Nodes", font=("Arial", 14))
labelKBC.grid(row=6, column=0, columnspan=3, pady=10)

labelRC = tk.Label(frameRC, text="Random Graph and Chromatic Coloring", font=("Arial", 14))
labelRC.pack(pady=10)

labelR = tk.Label(frameR, text="Random Graph", font=("Arial", 14))
labelR.pack(pady=10)

labelW = tk.Label(frameW, text="Walk in the Graph", font=("Arial", 14))
labelW.pack(pady=10)

labelIE = tk.Label(frameIE, text="Import and Export \nthe Graph", font=("Arial", 14))
labelIE.pack(pady=10)

# Add node
entryK = tk.Entry(frameKB)
entryK.grid(row=1, column=0, pady=10)
buttonK = tk.Button(frameKB, text="Add node", command=add_node)
buttonK.grid(row=1, column=1, padx=10, pady=10)

# Add edge
entryB1 = tk.Entry(frameKB)
entryB1.grid(row=2, column=0, pady=10)
entryB2 = tk.Entry(frameKB)
entryB2.grid(row=2, column=1, pady=10)
buttonB = tk.Button(frameKB, text="Add edge", command=add_edge)
buttonB.grid(row=2, column=2, padx=10, pady=10)

# Close button
buttonS = tk.Button(frameE, text="Close app", command=close_app)
buttonS.pack(side=tk.RIGHT, anchor=tk.N, padx=10, pady=10)

# Apply chromatic coloring
buttonC = tk.Button(frameRC, text="Chromatic coloring", command=toggle_chromatic, bg="red")
buttonC.pack(pady=10)
labelC = tk.Label(frameRC, text="")
labelC.pack()

# Walk from A to B
buttonW = tk.Button(frameW, text="Walk from A to B", command=walk)
buttonW.pack()
entryW1 = tk.Entry(frameW)
entryW1.pack()
entryW2 = tk.Entry(frameW)
entryW2.pack()
labelW = tk.Label(frameW, text="", wraplength=200)
labelW.pack()

# Check Euler graph
buttonE = tk.Button(frameRC, text="Euler graph", command=euler_graph)
buttonE.pack()
labelE1 = tk.Label(frameRC, text="")
labelE1.pack()
labelE2 = tk.Label(frameRC, text="", wraplength=300)
labelE2.pack(padx=10)

# Random graph
buttonR = tk.Button(frameR, text="Random graph", command=random_graph)
buttonR.pack()
entryR = tk.Entry(frameR)
entryR.pack()

# Clear graph
buttonCl = tk.Button(frameR, text="Clear graph", command=clear_graph)
buttonCl.pack(pady=10)

# Import file
buttonI = tk.Button(frameIE, text="Import graph", command=button_read_graph)
buttonI.pack(pady=10)
# Export file
buttonE = tk.Button(frameIE, text="Export graph", command=save_graph)
buttonE.pack(pady=10)

# File name input for import/export
labelN = tk.Label(frameIE, text="File name", font=("Arial", 12))
labelN.pack(pady=5)
entryN = tk.Entry(frameIE)
entryN.pack()

# Label for import/export status
labelIE = tk.Label(frameIE, text="")
labelIE.pack(pady=10)

# Button to remove nodes
buttonRK = tk.Button(frameKB, text="Remove node", command=remove_node)
buttonRK.grid(row=4, column=1, padx=10)
entryRK = tk.Entry(frameKB)
entryRK.grid(row=4, column=0, padx=5)

# Button to remove edges
buttonRB = tk.Button(frameKB, text="Remove edge", command=remove_edge)
buttonRB.grid(row=5, column=2, padx=10)
entryRB1 = tk.Entry(frameKB)
entryRB1.grid(row=5, column=0, padx=5)
entryRB2 = tk.Entry(frameKB)
entryRB2.grid(row=5, column=1, padx=5)

# Button to color nodes
buttonCK = tk.Button(frameKB, text="Color node", command=color_node)
buttonCK.grid(row=8, column=2, padx=10)
entryCKC = tk.Entry(frameKB)
entryCKC.grid(row=8, column=0, padx=5)
entryCKK = tk.Entry(frameKB)
entryCKK.grid(row=8, column=1, padx=5)

labelCKC = tk.Label(frameKB, text="color")
labelCKC.grid(row=7, column=0)
labelCKK = tk.Label(frameKB, text="node")
labelCKK.grid(row=7, column=1)


# First calls
plt.ion()
draw()
root.mainloop()