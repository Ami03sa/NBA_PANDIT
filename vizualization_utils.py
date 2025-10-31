import matplotlib.pyplot as plt
import numpy as np
import base64, io, re, matplotlib
matplotlib.use("Agg")

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)
    return img

def create_bar_chart(data):
    """Fixed: Proper Y-axis numbers, readable spacing."""
    plt.close("all")
    labels = data.get("labels", [])
    series = {k: v for k, v in data.items() if isinstance(v, list) and all(isinstance(x, (int, float)) for x in v)}

    if not labels or not series:
        return None

    fig, ax = plt.subplots(figsize=(7, 4))
    width = 0.8 / max(len(series), 1)
    x = np.arange(len(labels))

    for i, (label, values) in enumerate(series.items()):
        ax.bar(x + i * width, values, width, label=label)

    ax.set_title(data.get("title", "Bar Chart"))
    ax.set_xticks(x + width * len(series) / 2)
    ax.set_xticklabels(labels, rotation=30, ha='right')
    ax.set_ylabel("Value")  # ✅ fix: show numeric axis name
    ax.legend()
    plt.tight_layout()
    return fig_to_base64(fig)

def create_line_chart(data):
    plt.close("all")
    labels = data.get("labels", [])
    if not labels:
        return None

    fig, ax = plt.subplots(figsize=(7, 4))
    for key, values in data.items():
        if isinstance(values, list) and all(isinstance(x, (int, float)) for x in values):
            ax.plot(labels, values, marker="o", label=key)

    ax.set_title(data.get("title", "Line Chart"))
    ax.set_ylabel("Value")
    ax.legend()
    plt.tight_layout()
    return fig_to_base64(fig)

def create_pie_chart(data):
    plt.close("all")
    stats = {k: v for k, v in data.items() if isinstance(v, (int, float))}
    if not stats:
        return None

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(stats.values(), labels=stats.keys(), autopct="%1.1f%%", startangle=90)
    ax.set_title(data.get("title", "Pie Chart"))
    plt.tight_layout()
    return fig_to_base64(fig)

def generate_chart_from_json(data):
    """Auto-detect chart type + filter out invalid Y-axis values."""
    plt.close("all")

    if not isinstance(data, dict):
        return None

    # Normalize
    if "datasets" in data and isinstance(data["datasets"], list):
        normalized = {
            "title": data.get("title", "NBA Chart"),
            "labels": data.get("labels", []),
            "type": data.get("type")
        }
        for ds in data["datasets"]:
            label = ds.get("label", "Series")
            values = ds.get("data", [])
            normalized[label] = values
        data = normalized

    labels = data.get("labels", [])
    title = data.get("title", "").lower()
    series = {k: v for k, v in data.items() if isinstance(v, list)}

    # 🔍 Stronger auto-detection
    chart_type = (data.get("type") or "").lower()
    if not chart_type:
        if len(series) == 1 and len(labels) <= 6:
            chart_type = "pie"
        elif any(re.search(r"(20\d{2}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|game|week)", str(l).lower()) for l in labels):
            chart_type = "line"
        elif "percentage" in title or "distribution" in title or "share" in title:
            chart_type = "pie"
        elif len(series) > 1:
            chart_type = "bar"
        else:
            chart_type = "bar"

    # ✅ Call correct chart
    if chart_type.startswith("bar"):
        return create_bar_chart(data)
    elif chart_type.startswith("line"):
        return create_line_chart(data)
    elif chart_type.startswith("pie"):
        return create_pie_chart(data)
    else:
        return create_bar_chart(data)
