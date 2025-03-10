"""
URL configuration for dataFreaks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from trajectoryFreaks import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("graph/",views.graph_view),
    path("graph_events/",views.graph_view_1),
    path("graph_live/",views.graph_view_live),
    path("table/", views.table),
    path("graph_traj/",views.graph_view_Traj),
     path("live-matlab-graph/", views.live_graph_page, name="live_graph_page"),
     path('run-mat/', views.run_mat, name='run-mat'),
      path('run-mat2/', views.run_mat2, name='run-mat2'),
      path('run-matLive/', views.run_mat_live, name='run-mat_live'),
      path('run-matTraj/', views.run_mat_Traj, name='run-mat_Traj'),
]
