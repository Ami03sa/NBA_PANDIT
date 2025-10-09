import matplotlib.pyplot as plt
import io
from PIL import Image
import numpy as np

def generate_chart_from_json(viz_json):
    """
    Converts visualization JSON into a matplotlib chart.
    Returns a PIL image.
    """
    try:
        chart_type = viz_json.get("visualization_type", "bar_chart").lower()
        title = viz_json.get("title", "NBA Visualization")
        data = viz_json.get("data", {})
        config = viz_json.get("config", {})

        labels = data.get("labels", [])
        series_names = [k for k in data.keys() if k != "labels"]
        if not labels or not series_names:
            print("⚠️ Empty labels or data series")
            return None

        colors = config.get("colors", plt.cm.tab10.colors[:len(series_names)])
        legend_labels = config.get("legend", series_names)
        title_font_size = config.get("title_font_size", 16)
        axis_font_size = config.get("axis_font_size", 12)

        plt.figure(figsize=(8, 5))
        plt.title(title, fontsize=title_font_size)

        if chart_type == "bar_chart":
            x = np.arange(len(labels))
            width = 0.8 / len(series_names)
            for i, name in enumerate(series_names):
                plt.bar(x + i * width, data[name], width=width, label=legend_labels[i], color=colors[i])
            plt.xticks(x + width * (len(series_names)-1)/2, labels, fontsize=axis_font_size)
            plt.yticks(fontsize=axis_font_size)
            plt.ylabel(config.get("y_axis_label", ""), fontsize=axis_font_size)
            plt.xlabel(config.get("x_axis_label", ""), fontsize=axis_font_size)
            plt.legend(fontsize=axis_font_size)

        elif chart_type == "line_chart":
            for i, name in enumerate(series_names):
                plt.plot(labels, data[name], marker='o', label=legend_labels[i], color=colors[i])
            plt.xticks(fontsize=axis_font_size)
            plt.yticks(fontsize=axis_font_size)
            plt.ylabel(config.get("y_axis_label", ""), fontsize=axis_font_size)
            plt.xlabel(config.get("x_axis_label", ""), fontsize=axis_font_size)
            plt.legend(fontsize=axis_font_size)

        elif chart_type == "pie_chart":
            values = [data[name][0] for name in series_names]
            plt.pie(values, labels=legend_labels, autopct="%1.1f%%", colors=colors)

        else:
            plt.bar(labels, data.get(series_names[0], []))

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        return Image.open(buf)

    except Exception as e:
        print(f"❌ Visualization generation failed: {e}")
        plt.close()
        return None
