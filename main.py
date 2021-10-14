import json
import matplotlib
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
from base64 import b64decode
from matplotlib import style, rcParams

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

style.use("seaborn-dark")
rcParams.update({"font.size": 15, "legend.frameon": True})

matplotlib.rc("axes", titlesize=14)
matplotlib.rc("legend", fontsize=13)

for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
    rcParams[param] = "#2F3136"

for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
    rcParams[param] = "0.9"

rcParams.update({'axes.titlesize': 22})

rcParams["lines.linewidth"] = 2

app = Flask(__name__)

COLOURS = ["#08F7FE", "#FE53BB", "#F5D300", "#00ff41"]


def create_figure(data):
    fig = Figure(figsize=data["figsize"])

    axis = fig.add_subplot(1, 1, 1)

    for i, y in enumerate(data["y_values"]):
        x = range(len(data["y_values"][y]))
        axis.plot(
            x, data["y_values"][y], label=y, marker="o", color=COLOURS[i % len(COLOURS)]
        )

    axis.grid(color="#35373d")

    fig.legend()
    axis.set_title(data["title"])
    fig.subplots_adjust(bottom=data["adjust"])

    return fig


@app.route("/")
def serve_img():
    raw_data = request.args.get("data")
    if raw_data is None:
        return {"error": "no data"}

    decoded_data = b64decode(raw_data.encode()).decode()

    data = json.loads(decoded_data)

    if len(data["y_values"]) > 50:
        return {"error": "graph data too large"}

    fig = create_figure(data)

    output = BytesIO()

    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
