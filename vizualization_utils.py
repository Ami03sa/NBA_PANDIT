# visualization_utils.py
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

def generate_chart_from_json(viz_json):
    chart_type = viz_json.get("visualization_type")
    data = viz_json.get("data", {})
    config = viz_json.get("config", {})

    if chart_type == "bar_chart":
        labels = data.get("labels", [])
        players = [key for key in data.keys() if key != "labels"]
        colors = config.get("colors", ["#00BFFF", "#FF4500"])
        bar_width = config.get("bar_width", 0.4)

        x = range(len(labels))
        fig, ax = plt.subplots(figsize=(8, 5))

        for i, player in enumerate(players):
            values = data[player]
            ax.bar([p + i*bar_width for p in x], values, width=bar_width, color=colors[i], label=player)

        ax.set_xticks([p + bar_width/2 for p in x])
        ax.set_xticklabels(labels)
        ax.set_ylabel(config.get("y_axis_label", "Values"))
        ax.set_xlabel(config.get("x_axis_label", "Statistics"))
        ax.set_title(config.get("title", ""), fontsize=config.get("title_font_size", 16))
        ax.legend()
        plt.tight_layout()

        # Convert to PIL Image for Gradio
        buf = BytesIO()
        plt.savefig(buf, format='PNG')
        buf.seek(0)
        image = Image.open(buf)
        plt.close(fig)
        return image

    else:
        raise ValueError(f"Unsupported visualization type: {chart_type}")
