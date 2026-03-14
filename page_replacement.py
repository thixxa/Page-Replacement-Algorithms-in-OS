# Page Replacement Algorithm 

# GROUP 18
# 2022/E/122 - RATHNAYAKA P.G.R.M.D.R.
# 2022/E/180 - PRASANJANA W.T.


import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_BG = "#0f172a"
CARD_BG = "#1e293b"
INNER_BG = "#111827"
BORDER = "#334155"
TEXT_MAIN = "#f8fafc"
TEXT_MUTED = "#94a3b8"

BTN_FIFO = "#2563eb"
BTN_FIFO_HOVER = "#1d4ed8"

BTN_LRU = "#0f766e"
BTN_LRU_HOVER = "#115e59"

BTN_LFU = "#7c3aed"
BTN_LFU_HOVER = "#6d28d9"

BTN_MFU = "#ea580c"
BTN_MFU_HOVER = "#c2410c"

BTN_COMPARE = "#16a34a"
BTN_COMPARE_HOVER = "#15803d"

BTN_SAMPLE = "#475569"
BTN_SAMPLE_HOVER = "#334155"

BTN_CLEAR = "#b91c1c"
BTN_CLEAR_HOVER = "#991b1b"


# Page Replacement Algorithms 

def add_trace_row(trace, step, page, frame_slots, status, replaced):
    trace.append(
        {
            "step": step,
            "page": page,
            "frames": frame_slots[:],
            "status": status,
            "replaced": "-" if replaced is None else replaced,
        }
    )

# FIFO Algorithm Simulation

def simulate_fifo(reference, frame_count):
    frame_slots = [None] * frame_count
    trace = []
    faults = 0
    hits = 0
    pointer = 0

    for step, page in enumerate(reference, start=1):
        if page in frame_slots:
            hits += 1
            add_trace_row(trace, step, page, frame_slots, "HIT", None)
            continue

        faults += 1
        replaced = None

        if None in frame_slots:
            idx = frame_slots.index(None)
            frame_slots[idx] = page
        else:
            replaced = frame_slots[pointer]
            frame_slots[pointer] = page
            pointer = (pointer + 1) % frame_count

        add_trace_row(trace, step, page, frame_slots, "FAULT", replaced)

    return faults, hits, trace

# LRU Algorithm Simulation

def simulate_lru(reference, frame_count):
    frame_slots = [None] * frame_count
    last_used = {}
    trace = []
    faults = 0
    hits = 0

    for step, page in enumerate(reference, start=1):
        if page in frame_slots:
            hits += 1
            last_used[page] = step
            add_trace_row(trace, step, page, frame_slots, "HIT", None)
            continue

        faults += 1
        replaced = None

        if None in frame_slots:
            idx = frame_slots.index(None)
            frame_slots[idx] = page
        else:
            victim_idx = min(
                range(frame_count),
                key=lambda i: last_used.get(frame_slots[i], -1)
            )
            replaced = frame_slots[victim_idx]
            frame_slots[victim_idx] = page

        last_used[page] = step
        add_trace_row(trace, step, page, frame_slots, "FAULT", replaced)

    return faults, hits, trace

# LFU and MFU Helper Function

def pick_freq_victim(frame_slots, freq, loaded_at, choose_max):
    candidates = [(i, p) for i, p in enumerate(frame_slots) if p is not None]

    if choose_max:
        target = max(freq[p] for _, p in candidates)
        equal = [(i, p) for i, p in candidates if freq[p] == target]
    else:
        target = min(freq[p] for _, p in candidates)
        equal = [(i, p) for i, p in candidates if freq[p] == target]

    return min(equal, key=lambda item: loaded_at[item[1]])[0]

# LFU Algorithm Simulation

def simulate_lfu(reference, frame_count):
    frame_slots = [None] * frame_count
    freq = {}
    loaded_at = {}
    trace = []
    faults = 0
    hits = 0

    for step, page in enumerate(reference, start=1):
        freq[page] = freq.get(page, 0) + 1

        if page in frame_slots:
            hits += 1
            add_trace_row(trace, step, page, frame_slots, "HIT", None)
            continue

        faults += 1
        replaced = None

        if None in frame_slots:
            idx = frame_slots.index(None)
            frame_slots[idx] = page
        else:
            victim_idx = pick_freq_victim(frame_slots, freq, loaded_at, choose_max=False)
            replaced = frame_slots[victim_idx]
            frame_slots[victim_idx] = page

        loaded_at[page] = step
        add_trace_row(trace, step, page, frame_slots, "FAULT", replaced)

    return faults, hits, trace

# MFU Algorithm Simulation

def simulate_mfu(reference, frame_count):
    frame_slots = [None] * frame_count
    freq = {}
    loaded_at = {}
    trace = []
    faults = 0
    hits = 0

    for step, page in enumerate(reference, start=1):
        freq[page] = freq.get(page, 0) + 1

        if page in frame_slots:
            hits += 1
            add_trace_row(trace, step, page, frame_slots, "HIT", None)
            continue

        faults += 1
        replaced = None

        if None in frame_slots:
            idx = frame_slots.index(None)
            frame_slots[idx] = page
        else:
            victim_idx = pick_freq_victim(frame_slots, freq, loaded_at, choose_max=True)
            replaced = frame_slots[victim_idx]
            frame_slots[victim_idx] = page

        loaded_at[page] = step
        add_trace_row(trace, step, page, frame_slots, "FAULT", replaced)

    return faults, hits, trace


# Input Handling 

def get_input():
    try:
        frames_text = frame_entry.get().strip()
        ref_text = ref_entry.get().strip()

        if not frames_text:
            messagebox.showerror("Error", "Please enter the number of frames.")
            return None, None

        if not ref_text:
            messagebox.showerror("Error", "Please enter the reference string.")
            return None, None

        frames = int(frames_text)
        if frames <= 0:
            messagebox.showerror("Error", "Number of frames must be greater than 0.")
            return None, None

        reference = list(map(int, ref_text.split()))
        return frames, reference

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Enter integers only.")
        return None, None


# Text + Graph Helpers 

def format_trace_text(name, faults, hits, trace, frames):
    step_w = 4
    ref_w = 5
    frame_w = 5
    status_w = 8
    replaced_w = 9

    headers = [("t", step_w), ("ref", ref_w)]
    headers += [(f"F{i}", frame_w) for i in range(1, frames + 1)]
    headers += [("status", status_w), ("replaced", replaced_w)]

    header_line = " | ".join(f"{title:<{width}}" for title, width in headers)
    lines = [f"\n--- {name} Trace ---", header_line, "-" * len(header_line)]

    for row in trace:
        line_values = [
            f"{row['step']:<{step_w}}",
            f"{row['page']:<{ref_w}}",
        ]

        for p in row["frames"]:
            line_values.append(f"{('-' if p is None else p)!s:<{frame_w}}")

        line_values.append(f"{row['status']:<{status_w}}")
        line_values.append(f"{row['replaced']:<{replaced_w}}")

        lines.append(" | ".join(line_values))

    lines.append(f"\n{name} Faults: {faults} | Hits: {hits}\n")
    return "\n".join(lines)


def append_output(text):
    output.configure(state="normal")
    output.insert("end", text)
    output.see("end")
    output.configure(state="disabled")


def clear_output_only():
    output.configure(state="normal")
    output.delete("1.0", "end")
    output.configure(state="disabled")


def set_status(text):
    status_label.configure(text=text)


def update_summary_cards(faults="-", hits="-", best="-"):
    fault_value.configure(text=str(faults))
    hit_value.configure(text=str(hits))
    best_value.configure(text=str(best))


def _draw_trace_row(algorithm_name, trace, frame_count, top_margin, show_algo_label=True):
    box_w = 52
    box_h = 52
    step_gap = 28
    left_margin = 28

    step_block_w = (frame_count * box_w) + ((frame_count - 1) * 8)

    if show_algo_label:
        graph_canvas.create_text(
            20,
            top_margin - 28,
            text=algorithm_name,
            anchor="w",
            fill=TEXT_MAIN,
            font=("Segoe UI", 14, "bold"),
        )

    for c, row in enumerate(trace):
        block_x = left_margin + c * (step_block_w + step_gap)

        graph_canvas.create_text(
            block_x + (step_block_w / 2),
            top_margin - 8,
            text=f"Step {row['step']}   Ref: {row['page']}",
            fill="#d1d5db",
            font=("Segoe UI", 10, "bold"),
        )

        status_color = "#2563eb" if row["status"] == "HIT" else "#dc2626"

        for f_idx in range(frame_count):
            x1 = block_x + f_idx * (box_w + 8)
            y1 = top_margin + 12
            x2 = x1 + box_w
            y2 = y1 + box_h

            graph_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=status_color,
                outline="#e5e7eb",
                width=1,
            )

            value = row["frames"][f_idx]
            graph_canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text="-" if value is None else str(value),
                fill="white",
                font=("Segoe UI", 13, "bold"),
            )

            graph_canvas.create_text(
                (x1 + x2) / 2,
                y2 + 14,
                text=f"F{f_idx + 1}",
                fill=TEXT_MUTED,
                font=("Segoe UI", 9),
            )

        graph_canvas.create_text(
            block_x + (step_block_w / 2),
            top_margin + box_h + 50,
            text=row["status"],
            fill="#86efac" if row["status"] == "HIT" else "#fca5a5",
            font=("Segoe UI", 10, "bold"),
        )

        if row["replaced"] != "-":
            graph_canvas.create_text(
                block_x + (step_block_w / 2),
                top_margin + box_h + 68,
                text=f"Replaced: {row['replaced']}",
                fill="#fcd34d",
                font=("Segoe UI", 9),
            )

    row_width = left_margin + len(trace) * (step_block_w + step_gap) + 40
    row_height = top_margin + box_h + 90
    return row_width, row_height


def draw_graph(algorithm_name, trace, frame_count):
    graph_canvas.delete("all")

    if not trace:
        return

    graph_canvas.create_text(
        20,
        24,
        text=f"{algorithm_name} - Graphical Trace",
        anchor="w",
        fill=TEXT_MAIN,
        font=("Segoe UI", 15, "bold"),
    )

    row_w, row_h = _draw_trace_row(
        algorithm_name,
        trace,
        frame_count,
        60,
        show_algo_label=False
    )

    graph_canvas.config(scrollregion=(0, 0, row_w, row_h + 20))
    graph_canvas.xview_moveto(0)
    graph_canvas.yview_moveto(0)


def draw_compare_graph(all_traces, frame_count):
    graph_canvas.delete("all")

    graph_canvas.create_text(
        20,
        24,
        text="Compare All Algorithms - Graph View",
        anchor="w",
        fill=TEXT_MAIN,
        font=("Segoe UI", 15, "bold"),
    )

    y = 92
    max_w = 0

    for algo_name in ["FIFO", "LRU", "LFU", "MFU"]:
        trace = all_traces.get(algo_name, [])
        row_w, row_h = _draw_trace_row(algo_name, trace, frame_count, y, show_algo_label=True)
        max_w = max(max_w, row_w)
        y = row_h + 25

    graph_canvas.config(scrollregion=(0, 0, max_w, y + 15))
    graph_canvas.xview_moveto(0)
    graph_canvas.yview_moveto(0)


# GUI Button Functions 

def run_algorithm(name, simulator):
    frames, reference = get_input()
    if reference is None:
        return

    faults, hits, trace = simulator(reference, frames)

    clear_output_only()
    append_output(format_trace_text(name, faults, hits, trace, frames))
    draw_graph(name, trace, frames)
    update_summary_cards(faults, hits, name)
    set_status(f"{name} completed successfully. Faults = {faults}, Hits = {hits}")


def run_fifo():
    run_algorithm("FIFO", simulate_fifo)


def run_lru():
    run_algorithm("LRU", simulate_lru)


def run_lfu():
    run_algorithm("LFU", simulate_lfu)


def run_mfu():
    run_algorithm("MFU", simulate_mfu)


def compare_all():
    frames, reference = get_input()
    if reference is None:
        return

    simulations = {
        "FIFO": simulate_fifo(reference, frames),
        "LRU": simulate_lru(reference, frames),
        "LFU": simulate_lfu(reference, frames),
        "MFU": simulate_mfu(reference, frames),
    }

    results = {algo: (data[0], data[1]) for algo, data in simulations.items()}

    min_faults = min(faults for faults, hits in results.values())
    best_algorithms = [algo for algo, (faults, hits) in results.items() if faults == min_faults]

    clear_output_only()
    append_output("\n=== Algorithm Comparison ===\n\n")
    for algo, (faults, hits) in results.items():
        append_output(f"{algo:<5} -> Faults: {faults:<3} | Hits: {hits:<3}\n")
    append_output(f"\nBest Algorithm(s): {', '.join(best_algorithms)}\n\n")

    all_traces = {algo: data[2] for algo, data in simulations.items()}
    draw_compare_graph(all_traces, frames)
    update_summary_cards("-", "-", ", ".join(best_algorithms))
    set_status(f"Comparison completed. Best Algorithm(s): {', '.join(best_algorithms)}")


def clear_output():
    clear_output_only()
    graph_canvas.delete("all")
    update_summary_cards("-", "-", "-")
    set_status("Cleared results and graph view.")


def insert_sample():
    frame_entry.delete(0, "end")
    frame_entry.insert(0, "3")

    ref_entry.delete(0, "end")
    ref_entry.insert(0, "7 0 1 2 0 3 0 4 2 3 0 3 2")

    set_status("Sample input inserted.")


def toggle_mode():
    current = ctk.get_appearance_mode()

    if current == "Dark":
        ctk.set_appearance_mode("light")
        mode_button.configure(text="Dark Mode")
        set_status("Light mode enabled.")
    else:
        ctk.set_appearance_mode("dark")
        mode_button.configure(text="Light Mode")
        set_status("Dark mode enabled.")


# Main Window

app = ctk.CTk()
app.title("Page Replacement Simulator")
app.geometry("1500x900")
app.minsize(1250, 760)


header = ctk.CTkFrame(app, corner_radius=18, fg_color=CARD_BG)
header.pack(fill="x", padx=18, pady=(16, 10))

title = ctk.CTkLabel(
    header,
    text="Page Replacement Algorithm Simulator",
    font=("Segoe UI", 30, "bold"),
    text_color=TEXT_MAIN
)
title.pack(pady=(6, 4))

subtitle = ctk.CTkLabel(
    header,
    text="Visual simulation of FIFO, LRU, LFU, and MFU page replacement strategies",
    font=("Segoe UI", 14),
    text_color=TEXT_MUTED
)
subtitle.pack(pady=(0, 10))

# Input Card 

input_card = ctk.CTkFrame(app, corner_radius=18, fg_color=CARD_BG)
input_card.pack(fill="x", padx=18, pady=(0, 12))

input_inner = ctk.CTkFrame(input_card, fg_color="transparent")
input_inner.pack(fill="x", padx=16, pady=16)

input_inner.grid_columnconfigure(0, weight=0)
input_inner.grid_columnconfigure(1, weight=1)
input_inner.grid_columnconfigure(2, weight=0)
input_inner.grid_columnconfigure(3, weight=3)

frame_label = ctk.CTkLabel(
    input_inner,
    text="Number of Frames",
    font=("Segoe UI", 14, "bold"),
    text_color=TEXT_MAIN
)
frame_label.grid(row=0, column=0, padx=(0, 10), pady=8, sticky="w")

frame_entry = ctk.CTkEntry(
    input_inner,
    width=120,
    height=38,
    font=("Segoe UI", 14),
    corner_radius=10
)
frame_entry.grid(row=0, column=1, padx=(0, 20), pady=8, sticky="w")

ref_label = ctk.CTkLabel(
    input_inner,
    text="Reference String",
    font=("Segoe UI", 14, "bold"),
    text_color=TEXT_MAIN
)
ref_label.grid(row=0, column=2, padx=(0, 10), pady=8, sticky="w")

ref_entry = ctk.CTkEntry(
    input_inner,
    height=38,
    font=("Segoe UI", 14),
    corner_radius=10,
    placeholder_text="Example: 7 0 1 2 0 3 0 4 2 3 0 3 2"
)
ref_entry.grid(row=0, column=3, padx=(0, 0), pady=8, sticky="ew")

# Buttons Card

button_card = ctk.CTkFrame(app, corner_radius=18, fg_color=CARD_BG)
button_card.pack(fill="x", padx=18, pady=(0, 12))

button_frame = ctk.CTkFrame(button_card, fg_color="transparent")
button_frame.pack(padx=16, pady=14)

ctk.CTkButton(
    button_frame, text="Run FIFO", command=run_fifo,
    width=130, height=40, corner_radius=12,
    fg_color=BTN_FIFO, hover_color=BTN_FIFO_HOVER
).grid(row=0, column=0, padx=8, pady=8)

ctk.CTkButton(
    button_frame, text="Run LRU", command=run_lru,
    width=130, height=40, corner_radius=12,
    fg_color=BTN_LRU, hover_color=BTN_LRU_HOVER
).grid(row=0, column=1, padx=8, pady=8)

ctk.CTkButton(
    button_frame, text="Run LFU", command=run_lfu,
    width=130, height=40, corner_radius=12,
    fg_color=BTN_LFU, hover_color=BTN_LFU_HOVER
).grid(row=0, column=2, padx=8, pady=8)

ctk.CTkButton(
    button_frame, text="Run MFU", command=run_mfu,
    width=130, height=40, corner_radius=12,
    fg_color=BTN_MFU, hover_color=BTN_MFU_HOVER
).grid(row=0, column=3, padx=8, pady=8)

ctk.CTkButton(
    button_frame, text="Compare All", command=compare_all,
    width=140, height=40, corner_radius=12,
    fg_color=BTN_COMPARE, hover_color=BTN_COMPARE_HOVER
).grid(row=0, column=4, padx=14, pady=8)

ctk.CTkButton(
    button_frame, text="Sample Input", command=insert_sample,
    width=140, height=40, corner_radius=12,
    fg_color=BTN_SAMPLE, hover_color=BTN_SAMPLE_HOVER
).grid(row=0, column=5, padx=8, pady=8)

ctk.CTkButton(
    button_frame, text="Clear", command=clear_output,
    width=120, height=40, corner_radius=12,
    fg_color=BTN_CLEAR, hover_color=BTN_CLEAR_HOVER
).grid(row=0, column=6, padx=8, pady=8)

# Summary Cards 

summary_frame = ctk.CTkFrame(app, corner_radius=18, fg_color="transparent")
summary_frame.pack(fill="x", padx=18, pady=(0, 10))

summary_frame.grid_columnconfigure(0, weight=1)
summary_frame.grid_columnconfigure(1, weight=1)
summary_frame.grid_columnconfigure(2, weight=1)

fault_card = ctk.CTkFrame(summary_frame, corner_radius=16, fg_color="#1d4ed8")
fault_card.grid(row=0, column=0, padx=6, pady=3, sticky="nsew")

hit_card = ctk.CTkFrame(summary_frame, corner_radius=16, fg_color="#15803d")
hit_card.grid(row=0, column=1, padx=6, pady=3, sticky="nsew")

best_card = ctk.CTkFrame(summary_frame, corner_radius=16, fg_color="#92400e")
best_card.grid(row=0, column=2, padx=6, pady=3, sticky="nsew")

fault_title = ctk.CTkLabel(
    fault_card, text="Page Faults",
    font=("Segoe UI", 13, "bold"),
    text_color="white"
)
fault_title.pack(pady=(10, 2))

fault_value = ctk.CTkLabel(
    fault_card, text="-",
    font=("Segoe UI", 22, "bold"),
    text_color="white"
)
fault_value.pack(pady=(0, 8))

hit_title = ctk.CTkLabel(
    hit_card, text="Hits",
    font=("Segoe UI", 13, "bold"),
    text_color="white"
)
hit_title.pack(pady=(10, 2))

hit_value = ctk.CTkLabel(
    hit_card, text="-",
    font=("Segoe UI", 22, "bold"),
    text_color="white"
)
hit_value.pack(pady=(0, 8))

best_title = ctk.CTkLabel(
    best_card, text="Best Algorithm",
    font=("Segoe UI", 13, "bold"),
    text_color="white"
)
best_title.pack(pady=(10, 2))

best_value = ctk.CTkLabel(
    best_card, text="-",
    font=("Segoe UI", 18, "bold"),
    text_color="white"
)
best_value.pack(pady=(0, 8))

# Main Content

main_views = ctk.CTkFrame(app, fg_color="transparent")
main_views.pack(fill="both", expand=True, padx=18, pady=(0, 12))
main_views.grid_columnconfigure(0, weight=1)
main_views.grid_columnconfigure(1, weight=1)
main_views.grid_rowconfigure(0, weight=1)

# Left panel
results_panel = ctk.CTkFrame(main_views, corner_radius=18, fg_color=CARD_BG)
results_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

results_title = ctk.CTkLabel(
    results_panel,
    text="Text Results",
    font=("Segoe UI", 18, "bold"),
    text_color=TEXT_MAIN
)
results_title.pack(anchor="w", padx=14, pady=(12, 6))

results_subtitle = ctk.CTkLabel(
    results_panel,
    text="Detailed page trace, page faults, and hits",
    font=("Segoe UI", 12),
    text_color=TEXT_MUTED
)
results_subtitle.pack(anchor="w", padx=14, pady=(0, 8))

output = ctk.CTkTextbox(
    results_panel,
    font=("Consolas", 13),
    corner_radius=12,
    wrap="none",
    fg_color=INNER_BG,
    text_color=TEXT_MAIN,
    border_width=1,
    border_color=BORDER
)
output.pack(fill="both", expand=True, padx=14, pady=(0, 14))
output.configure(state="disabled")

# Right panel
graph_panel = ctk.CTkFrame(main_views, corner_radius=18, fg_color=CARD_BG)
graph_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

graph_title = ctk.CTkLabel(
    graph_panel,
    text="Graphical Visualization",
    font=("Segoe UI", 18, "bold"),
    text_color=TEXT_MAIN
)
graph_title.pack(anchor="w", padx=14, pady=(12, 6))

graph_subtitle = ctk.CTkLabel(
    graph_panel,
    text="Blue = HIT   |   Red = FAULT",
    font=("Segoe UI", 12),
    text_color=TEXT_MUTED
)
graph_subtitle.pack(anchor="w", padx=14, pady=(0, 8))

graph_container = ctk.CTkFrame(
    graph_panel,
    corner_radius=12,
    fg_color=INNER_BG
)
graph_container.pack(fill="both", expand=True, padx=14, pady=(0, 14))

graph_container.grid_rowconfigure(0, weight=1)
graph_container.grid_columnconfigure(0, weight=1)

graph_canvas = tk.Canvas(
    graph_container,
    bg=INNER_BG,
    highlightthickness=0,
    relief="flat",
)
graph_canvas.grid(row=0, column=0, sticky="nsew")

v_scroll = ctk.CTkScrollbar(
    graph_container,
    orientation="vertical",
    command=graph_canvas.yview
)
v_scroll.grid(row=0, column=1, sticky="ns")

h_scroll = ctk.CTkScrollbar(
    graph_container,
    orientation="horizontal",
    command=graph_canvas.xview
)
h_scroll.grid(row=1, column=0, sticky="ew")

graph_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

# Status Bar 

status_bar = ctk.CTkFrame(app, corner_radius=14, fg_color=CARD_BG)
status_bar.pack(fill="x", padx=18, pady=(0, 16))

status_label = ctk.CTkLabel(
    status_bar,
    text="Ready. Enter frames and reference string, then run an algorithm.",
    font=("Segoe UI", 12),
    anchor="w",
    text_color=TEXT_MAIN
)
status_label.pack(fill="x", padx=12, pady=8)

# Default Startup

insert_sample()
update_summary_cards("-", "-", "-")

# Run the application

app.mainloop()