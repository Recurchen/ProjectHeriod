from audioop import avg
from math import ceil
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms.forms import NewRecordForm
from django.contrib.auth.models import User
from .models import Record
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import math

# Create your views here.


class NewRecordView(FormView):
    template_name = 'form.html'
    form_class = NewRecordForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(status=401)

    def form_valid(self, form):
        user_id = self.request.user.id
        curr_user = User.objects.get(id = user_id)
        new_record = Record.objects.create(
            date = form.cleaned_data["date"],
            period = form.cleaned_data["period"],
            user = curr_user)
        return HttpResponseRedirect(f"/records/estimate/")


def EstimateView(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            latest_record = Record.objects.filter(user = request.user).order_by("-date")[0]
            latest_date = latest_record.date
            estimate_date = latest_date + datetime.timedelta(days = 30)

            latest_six_records = Record.objects.filter(user = request.user).order_by("-date")[:5]
            avg_length = 0
            count  = 0
            for record in latest_six_records:
                avg_length += record.period
                count += 1
            
            avg_length = avg_length / count
            min_length = math.floor(avg_length)
            max_length = ceil(avg_length)
            
            return JsonResponse({"next period": estimate_date, 
                                "period will last": str(min_length) + ' to ' + str(max_length) + ' days'})
    else:
        return HttpResponse(status=401)

