from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "t.html")

def graph_view(request):
    # Create the plot
    plt.figure(figsize=(5, 3))
    x = [1, 2, 3, 4, 5]
    y = [10, 12, 15, 20, 25]
    plt.plot(x, y, marker='o', linestyle='-')
    plt.title("Sample Graph")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    uri = "data:image/png;base64," + string  # Convert to data URI

    return render(request, "grapht.html", {"graph": uri})
