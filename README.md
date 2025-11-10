# 📊 Vertex Cover on Snark Graphs

This project uses Python and the Google OR-Tools library to model and solve the **Minimum Vertex Cover** problem on Snark graphs.

The script includes generators for two specific types of Snarks:
* **Flower Snark (J_n)**
* **Goldberg Snark**

The solver uses Mixed-Integer Programming (MIP) to find the smallest set of vertices that "covers" every edge in the graph.

---

## ⚙️ Requirements

* Python 3.x
* Google OR-Tools library

To install the necessary dependency, run:

```bash
pip install ortools
