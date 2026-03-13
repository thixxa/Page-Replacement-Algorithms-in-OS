# Page Replacement Algorithm Simulator

A Python-based graphical user interface (GUI) application to simulate and visualize various Page Replacement Algorithms used in Operating Systems.

## 🚀 Features

- **Four Supported Algorithms**:
  - First In First Out (FIFO)
  - Least Recently Used (LRU)
  - Least Frequently Used (LFU)
  - Most Frequently Used (MFU)
- **Interactive GUI**: Built using `customtkinter`, providing a modern, smooth, and clean dark/light UI.
- **Detailed Traces**:
  - **Textual Trace View**: Displays a step-by-step trace of frame contents, page hits, page faults, and replaced pages.
  - **Graphical Visualization**: Color-coded visualization (Blue for HIT, Red for FAULT) to intuitively see the page replacement lifecycle.
- **Algorithm Comparison**: Run all four algorithms on the same reference string simultaneously to find the optimal memory management strategy holding the least page faults.
- **Sample Input**: One-click sample input insertion to quickly demonstrate functionality.

## 🛠️ Requirements

- Python 3.x
- `customtkinter`

You can install `customtkinter` via pip:

```bash
pip install customtkinter
```

## 🎮 How to Run

1. Clone or download this project.
2. Navigate to the directory containing the project.
3. Run the python script:

```bash
python page_replacement.py
```

## 📝 Usage Instructions

1. **Number of Frames**: Enter the total number of memory frames available (e.g., `3` or `4`).
2. **Reference String**: Enter a space-separated list of page requests (e.g., `7 0 1 2 0 3 0 4 2 3 0 3 2`).
3. **Execute**: 
   - Click "Run FIFO", "Run LRU", "Run LFU", or "Run MFU" to see the simulation for a specific algorithm.
   - Click "Compare All" to run your reference string against every algorithm to see a side-by-side comparison of faults, hits, and traces.
4. **View Results**: Trace details are present in the "Text Results" panel, and the color-coded visual graph can be horizontally scrolled in the "Graphical Visualization" panel.

