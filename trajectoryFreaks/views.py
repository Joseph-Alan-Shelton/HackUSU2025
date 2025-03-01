from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from . import mat2
from . import mat
from . import matLive
from . import matTraj
import json
from django.http import JsonResponse
import multiprocessing
import os
import sys
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from basicServer import SQL # Now import SQL from basicServer

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
    filename = 'trajectoryFreaks/mat2.py'
    with open(filename) as file:
        exec(file.read())

    
    mat2.main(0,100)  # Assuming there's a function named 'main' in script2.py

    """ import subprocess
    subprocess.run(['python', filename]) """

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


def run_mat_live(request):
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

def graph_view_live(request):
    process = multiprocessing.Process(target=matLive.main, args=(0, 1000))
    process.start()  # Runs in the background

    return render(request, "liveGrapht.html")

def table(request):
    # Initialize sql connection
    s = SQL()

    # Get the positions within our bounds
    q = f"""
        SELECT maneuverId, ManeuverPlan.secondsSinceStart, WaypointX, WaypointY, WaypointZ
        FROM ManeuverPlan JOIN RpoPlan 
        on ManeuverPlan.secondsSinceStart = RpoPlan.secondsSinceStart 
        where ? <= RpoPlan.secondsSinceStart And RpoPlan.secondsSinceStart <= ? 
        ORDER BY (select RpoPlan.secondsSinceStart);
        """
    maneuverData = s.query(q,(0, 1400563.295))

    q = f"""
        SELECT eventId, startSeconds, stopSeconds, eventType
        FROM PayloadEvents
        where ? <= startSeconds Or stopSeconds <= ?;
        """
    payloadData = s.query(q,(0, 1400563.295))

    q = f"""
        SELECT contactId, startSeconds, stopSeconds, groundSite
        FROM GroundContacts 
        where ? <= startSeconds Or stopSeconds <= ?;
        """
    groundData = s.query(q,(0, 1400563.295))

    context = {
        'ManeuverData':maneuverData,
        'PayloadData':payloadData,
        'GroundData':groundData
    }
    
    return render(request, "table.html", context)

def run_mat_Traj(request):
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

def graph_view_Traj(request):
    process = multiprocessing.Process(target=matTraj.main, args=(0, 100))
    process.start()  # Runs in the background

    return render(request, "TrajGrapht.html")
