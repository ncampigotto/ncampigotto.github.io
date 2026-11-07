"""Create the three English vector plots for the day-care fine slides.

The plotted values are digitized approximately from fineprice_1–3.png.
The 1–20 week and 0–25 pickup scales match the other slides in this sequence.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


TREATMENT = [
    8.4, 7.9, 8.0, 7.8, 6.5,
    11.3, 14.1, 17.2, 20.2, 14.2, 18.0, 18.0,
    19.1, 19.8, 19.5, 19.1, 16.2, 19.2, 20.6, 18.9,
]
CONTROL = [
    9.3, 9.0, 12.0, 9.8, 6.8,
    9.5, 9.3, 10.8, 9.0, 10.5, 8.3, 8.8,
    9.3, 9.3, 11.8, 7.8, 6.8, 9.5, 7.5, 9.3,
]
RED = "#d62728"
BLUE = "#1f77b4"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "svg.fonttype": "none",  # Keep labels as selectable, editable SVG text.
})

def make_chart(last_week, filename):
    fig = plt.figure(figsize=(12, 6.48), facecolor="white")
    ax = fig.add_axes([0.093, 0.139, 0.897, 0.728])
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 25)
    ax.set_xticks(range(1, 21))
    ax.set_yticks(range(0, 26, 5))
    ax.grid(axis="y", color="#bdbdbd", linewidth=0.8)
    ax.set_axisbelow(True)

    weeks = range(1, last_week + 1)
    ax.plot(weeks, TREATMENT[:last_week], color=RED, marker="s", markersize=12,
            linewidth=2.0, zorder=3)
    ax.plot(weeks, CONTROL[:last_week], color=BLUE, marker="D", markersize=11,
            linewidth=2.0, zorder=4)

    if last_week > 5:
        ax.axvline(5, color="#9e9e9e", linestyle=(0, (6, 5)), linewidth=0.9,
                   zorder=1)
        ax.text(5.2, 22.6, "Fines introduced", fontsize=18, va="center")
    if last_week > 17:
        ax.axvline(17, color="#9e9e9e", linestyle=(0, (6, 5)), linewidth=0.9,
                   zorder=1)
        ax.text(17.2, 22.6, "Fines removed", fontsize=18, va="center")

    ax.set_xlabel("Week", fontsize=25, labelpad=10)
    ax.set_ylabel("Number of late pickups", fontsize=25, labelpad=10)
    ax.tick_params(axis="both", which="major", direction="in", top=True,
                   right=True, labelsize=21, length=10, width=0.8, pad=7)
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)

    handles = [
        Line2D([], [], color=RED, marker="s", linestyle="None", markersize=14,
               label="Treatment group with fines"),
        Line2D([], [], color=BLUE, marker="s", linestyle="None", markersize=14,
               label="Control group without fines"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.12, 0.98),
               ncol=2, frameon=False, fontsize=20, handletextpad=0.5,
               columnspacing=3.0)

    fig.savefig(Path(__file__).with_name(filename), format="svg",
                facecolor="white")
    plt.close(fig)


for last_week, filename in (
    (5, "fineprice_1_en.svg"),
    (17, "fineprice_2_en.svg"),
    (20, "fineprice_3_en.svg"),
):
    make_chart(last_week, filename)
