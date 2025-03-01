from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from . import mat2
from . import mat
import json
from django.http import JsonResponse
import multiprocessing
# Create your views here.
def index(request):
    return render(request, "main.html")


def live_graph_page(request):
    return render(request, "liveGrapht.html")


def run_mat2(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lower = int(data.get("lower"))
            upper = int(data.get("upper"))

            if lower >= upper:
                return JsonResponse({"error": "Lower bound must be less than upper bound"}, status=400)

            process = multiprocessing.Process(target=mat2.main, args=(lower, upper))
            process.start()

            return JsonResponse({"message": f"Bounds updated to {lower}s - {upper}s"})

        except (ValueError, TypeError, KeyError):
            return JsonResponse({"error": "Invalid input data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def graph_view(request):
    process = multiprocessing.Process(target=mat2.main, args=(0, 100))
    process.start()  # Runs in the background

    return render(request, "liveGrapht.html")


def run_mat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lower = int(data.get("lower"))
            upper = int(data.get("upper"))

            if lower >= upper:
                return JsonResponse({"error": "Lower bound must be less than upper bound"}, status=400)

            process = multiprocessing.Process(target=mat.main, args=(lower, upper))
            process.start()

            return JsonResponse({"message": f"Bounds updated to {lower}s - {upper}s"})

        except (ValueError, TypeError, KeyError):
            return JsonResponse({"error": "Invalid input data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def graph_view_1(request):
    filename = 'trajectoryFreaks/mat.py'
    with open(filename) as file:
        exec(file.read())

    
    mat.main(0,100)  # Assuming there's a function named 'main' in script2.py

    """ import subprocess
    subprocess.run(['python', filename]) """

    return render(request, "liveGrapht_1.html")
