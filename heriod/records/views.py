from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms.forms import NewRecordForm
from django.contrib.auth.models import User
from .models import Record
from django.http import HttpResponse, HttpResponseRedirect

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
        return HttpResponseRedirect(f"/records/successfuladd/")


def SuccessAdd():
    return HttpResponse("success")
