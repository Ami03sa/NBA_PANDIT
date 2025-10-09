import matplotlib.pyplot as plt
import io
from PIL import Image

def generate_chart_from_json(viz_json):
    """
    Generates a matplotlib chart based on visualization JSON structure.
    Returns a PIL image for Gradio.
    Expected JSON keys: {"type": "bar"|"line"|"pie", "x": [...], "y": [...], "title": "..."}
    """
    chart_type = viz_json.get("type", "bar").lower()
    x = viz_json.get("x", [])
    y = viz_json.get("y", [])
    title = viz_json.get("title", "NBA Visualization")

    plt.figure(figsize=(6, 4))
    plt.title(title)

    try:
        if chart_type == "bar":
            plt.bar(x, y)
        elif chart_type == "line":
            plt.plot(x, y, marker='o')
        elif chart_type == "pie":
            plt.pie(y, labels=x, autopct="%1.1f%%")
        else:
            plt.bar(x, y)  # default fallback

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
