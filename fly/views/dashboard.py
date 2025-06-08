from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

from fly import models as fly_models
from fly.utils import pagination

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')