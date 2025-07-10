import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def generate_graph(expression, x_range=(-10, 10)):
    x_vals = np.linspace(x_range[0], x_range[1], 400)
    try:
        y_vals = eval(expression.replace("x", "x_vals"))
    except Exception as e:
        return { "success": False, "error": f"Graphing failed: {str(e)}" }

    plt.figure(figsize=(6, 4))
    plt.plot(x_vals, y_vals, label=expression)
    plt.title(f"Graph of {expression}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    graph_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return {
        "success": True,
        "image": f"data:image/png;base64,{graph_base64}"
    }
