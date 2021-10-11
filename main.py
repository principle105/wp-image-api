import json
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
from base64 import b64decode
from matplotlib import style

style.use("fivethirtyeight")

app = Flask(__name__)

def create_figure(data):
    fig = Figure(figsize=data["figsize"])

    axis = fig.add_subplot(1, 1, 1)

    for y in data["y_values"]:
        x = range(len(data["y_values"][y]))
        axis.plot(x, data["y_values"][y], label=y)

    fig.legend()
    fig.title(data["title"])
    fig.subplots_adjust(bottom=data["adjust"])

    return fig

@app.route("/")
def serve_img():
    raw_data = request.args.get("data")
    if raw_data is None:
      return {"error": "no data"}

    decoded_data = b64decode(raw_data.encode()).decode()

    data = json.loads(decoded_data)

    fig = create_figure(data)

    output = BytesIO()

    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
