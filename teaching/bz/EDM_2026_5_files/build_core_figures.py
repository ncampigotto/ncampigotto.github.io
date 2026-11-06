"""Build slide-sized SVG redraws of CORE Econ Microeconomics Figures 4.16–4.20.

The bar values are read from the original CORE SVGs (rounded to whole percent).
Sources:
https://books.core-econ.org/the-economy/microeconomics/04-strategic-interactions-11-ultimatum-game.html
https://books.core-econ.org/the-economy/microeconomics/04-strategic-interactions-12-experimental-results.html
"""

from pathlib import Path
from xml.etree import ElementTree as ET


HERE = Path(__file__).parent
FONT = "Roboto, Arial, sans-serif"
INK = "#131516"
MUTED = "#586168"
GRID = "#d9dfe3"
FARMER = "#ed1f24"
STUDENT = "#3a53a4"
DARK_FARMER = "#980004"
DARK_STUDENT = "#122a73"


def element(parent, name, **attrs):
    return ET.SubElement(parent, name, {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def label(parent, x, y, value, size=22, anchor="middle", fill=INK, weight=None, **attrs):
    options = dict(x=x, y=y, fill=fill, font_family=FONT, font_size=size, text_anchor=anchor)
    if weight:
        options["font_weight"] = weight
    options.update(attrs)
    node = element(parent, "text", **options)
    node.text = value
    return node


def canvas(width, height, description):
    root = ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-label": description,
        },
    )
    element(root, "rect", x=0, y=0, width=width, height=height, fill="white")
    return root


def save(root, name):
    ET.indent(root)
    ET.ElementTree(root).write(HERE / name, encoding="utf-8", xml_declaration=True)


def game_tree():
    root = canvas(1000, 470, "Game tree for the ultimatum game with equal and unequal offers")
    root.set("class", "ultimatum-tree")
    root.set("style", "display:block;width:91%;max-width:1000px;height:auto;margin:0 auto")
    rules = [
        ".ultimatum-tree .edge { transition: stroke 180ms ease, stroke-width 180ms ease; }",
        ".ultimatum-tree .payoff-box, .ultimatum-tree .proposer-node, "
        ".ultimatum-tree .responder-node { transition: fill 180ms ease; }",
        ".ultimatum-tree .terminal { cursor: pointer; }",
        ".ultimatum-tree .edge { pointer-events: none; }",
    ]
    for index in range(4):
        branch = "fair" if index < 2 else "unfair"
        highlight_fill = "#cfe9df" if index % 2 == 0 else "#dfe3e6"
        active = f".ultimatum-tree:has(.terminal-{index}:is(:hover,:focus-visible))"
        rules.append(
            f"{active} .edge-{branch}, {active} .edge-outcome-{index} "
            "{ stroke: #4d5aac; stroke-width: 7; }"
        )
        rules.append(
            f"{active} .terminal-{index} .payoff-box "
            f"{{ fill: {highlight_fill}; }}"
        )
        rules.append(
            f"{active} .proposer-node {{ fill: #dce2f7; }} "
            f"{active} .responder-{branch} {{ fill: #d4ecef; }} "
            f"{active} .offer-{branch} {{ font-weight: bold; }} "
            f"{active} .action-{index} {{ fill: #107895; font-weight: bold; }}"
        )
    style = ET.Element("style")
    style.text = "\n".join(rules)
    root.insert(0, style)

    element(root, "rect", x=356, y=16, width=288, height=54, rx=14,
            fill="#edf0f9", **{"class": "proposer-node"})
    label(root, 500, 51, "PROPOSER", 24, weight="bold", fill="#4d5aac").set(
        "class", "proposer-label"
    )

    for x2, offer, branch in [(270, "Offer (50, 50)", "fair"),
                              (730, "Offer (80, 20)", "unfair")]:
        element(root, "line", x1=500, y1=70, x2=x2, y2=155,
                stroke=MUTED, stroke_width=3,
                **{"class": f"edge edge-{branch}"})
        midpoint = (500 + x2) / 2
        element(root, "rect", x=midpoint - 85, y=93, width=170, height=32, fill="white")
        label(root, midpoint, 117, offer, 23, fill="#4d5aac").set(
            "class", f"offer-label offer-{branch}"
        )
        element(root, "rect", x=x2 - 89, y=155, width=178, height=58, rx=20,
                fill="#e8f4f6", **{"class": f"responder-node responder-{branch}"})
        label(root, x2, 193, "RESPONDER", 24, weight="bold", fill="#107895").set(
            "class", f"responder-label responder-label-{branch}"
        )

    # Outcomes are ordered from left to right. Payoffs are (Proposer, Responder).
    outcomes = [
        (270, 145, "Accept", "(50, 50)"),
        (270, 395, "Reject", "(0, 0)"),
        (730, 605, "Accept", "(80, 20)"),
        (730, 855, "Reject", "(0, 0)"),
    ]
    for index, (start, end, action, payoff) in enumerate(outcomes):
        element(root, "line", x1=start, y1=213, x2=end, y2=318,
                stroke=MUTED, stroke_width=3,
                **{"class": f"edge edge-outcome-{index}"})
        midpoint = (start + end) / 2
        element(root, "rect", x=midpoint - 45, y=263, width=90, height=30, fill="white")
        label(root, midpoint, 286, action, 22, fill="#107895").set(
            "class", f"action-label action-{index}"
        )
        terminal = element(root, "g", tabindex=0, role="group",
                           aria_label=f"{action} offer with payoff {payoff}",
                           **{"class": f"terminal terminal-{index}"})
        element(terminal, "rect", x=end - 101, y=324, width=202, height=71, rx=11,
                fill="#f3f5f6",
                **{"class": "payoff-box"})
        label(terminal, end, 369, payoff, 28, weight="bold").set("class", "payoff-text")
    label(root, 500, 448, "Payoffs shown as (Proposer, Responder)", 21, fill=MUTED)
    (HERE / "core_figure_4_16.html").write_text(
        "```{=html}\n" + ET.tostring(root, encoding="unicode") + "\n```\n",
        encoding="utf-8",
    )


def grouped_chart(name, description, xvalues, series, ymax, ticks, ylabel, xlabel,
                  rejected=None, height=520):
    root = canvas(1000, height, description)
    left, right, top, bottom = 100, 970, 75, height - 100
    plot_height = bottom - top

    for tick in ticks:
        y = bottom - tick / ymax * plot_height
        element(root, "line", x1=left, y1=f"{y:.2f}", x2=right, y2=f"{y:.2f}",
                stroke=GRID, stroke_width=1.5)
        label(root, left - 18, y + 7, str(tick), 19, anchor="end", fill=MUTED)

    element(root, "line", x1=left, y1=top, x2=left, y2=bottom, stroke=INK, stroke_width=2)
    element(root, "line", x1=left, y1=bottom, x2=right, y2=bottom, stroke=INK, stroke_width=2)

    n = len(xvalues)
    gap = (right - left - 100) / (n - 1)
    bar_width = 28 if n <= 6 else 19
    for i, value in enumerate(xvalues):
        centre = left + 50 + gap * i
        label(root, centre, bottom + 31, str(value), 21)
        for side, (legend, values, color, dark) in enumerate(series):
            bar_x = centre + (side - 1) * bar_width
            bar_height = values[i] / ymax * plot_height
            y = bottom - bar_height
            rect = element(root, "rect", x=f"{bar_x:.2f}", y=f"{y:.2f}",
                           width=bar_width, height=f"{bar_height:.2f}", fill=color)
            element(rect, "title").text = f"{legend}: {value}% offer, {values[i]}%"
            if rejected is not None:
                dark_height = values[i] * rejected[side][i] / 100 / ymax * plot_height
                element(root, "rect", x=f"{bar_x:.2f}", y=f"{bottom - dark_height:.2f}",
                        width=bar_width, height=f"{dark_height:.2f}", fill=dark)

    label(root, (left + right) / 2, height - 20, xlabel, 21)
    label(root, 29, (top + bottom) / 2, ylabel, 20,
          transform=f"rotate(-90 29 {(top + bottom) / 2})")

    legend_y = 24
    for i, (legend, _, color, dark) in enumerate(series):
        x = 100 + i * 280
        element(root, "rect", x=x, y=legend_y - 15, width=20, height=20, fill=color)
        label(root, x + 30, legend_y + 2, legend, 21, anchor="start")
    if rejected is not None:
        element(root, "rect", x=680, y=legend_y - 15, width=20, height=20, fill=DARK_FARMER)
        element(root, "rect", x=704, y=legend_y - 15, width=20, height=20, fill=DARK_STUDENT)
        label(root, 734, legend_y + 2, "Darker = rejected", 20, anchor="start")
    save(root, name)


def charts():
    offers = [0, 10, 20, 30, 40, 50]
    grouped_chart(
        "core_figure_4_17.svg",
        "Share of responders who would accept each offer, Kenyan farmers versus Emory students",
        offers,
        [("Kenyan farmers", [0, 2, 10, 52, 96, 100], FARMER, DARK_FARMER),
         ("Emory students", [0, 58, 63, 84, 89, 100], STUDENT, DARK_STUDENT)],
        100, [0, 25, 50, 75, 100],
        "Responders accepting (%)", "Share of pie offered to Responder (%)",
    )

    proposer_series = [
        ("Kenyan farmers", [4, 12, 10, 14, 50, 10], FARMER, DARK_FARMER),
        ("Emory students", [21, 11, 21, 37, 5, 5], STUDENT, DARK_STUDENT),
    ]
    grouped_chart(
        "core_figure_4_18a.svg",
        "Distribution of offers made by Kenyan farmer and Emory student proposers",
        offers, proposer_series, 60, [0, 15, 30, 45, 60],
        "Proposers making offer (%)", "Share of pie offered to Responder (%)",
    )
    grouped_chart(
        "core_figure_4_18b.svg",
        "Distribution of offers, with rejected shares shown in darker colors",
        offers, proposer_series, 60, [0, 15, 30, 45, 60],
        "Proposers making offer (%)", "Share of pie offered to Responder (%)",
        rejected=[[100, 98, 90, 48, 4, 0], [100, 42, 37, 16, 10, 0]],
    )
    grouped_chart(
        "core_figure_4_20.svg",
        "Share of responders rejecting each offer, with one responder or two competing responders",
        list(range(0, 55, 5)),
        [("One Responder", [100, 100, 80, 80, 80, 59, 40, 37, 19, 10, 0], FARMER, DARK_FARMER),
         ("Two Responders", [75, 58, 56, 45, 29, 23, 9, 8, 19, 16, 0], STUDENT, DARK_STUDENT)],
        100, [0, 25, 50, 75, 100],
        "Responders rejecting (%)", "Share of pie offered to Responder (%)",
    )


if __name__ == "__main__":
    game_tree()
    charts()
