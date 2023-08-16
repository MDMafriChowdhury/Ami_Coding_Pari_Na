from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import views as auth_views
from .forms import KhojSearchForm
from .models import InputValue


from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/login.html' 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def khoj_search(request):
    if request.method == 'POST':
        form = KhojSearchForm(request.POST)
        if form.is_valid():
            input_values_str = form.cleaned_data['input_values']
            search_value = form.cleaned_data['search_value']

            input_values = [int(value) for value in input_values_str.split(',')]
            input_values.sort(reverse=True)
            input_values_str = ', '.join(str(value) for value in input_values)

            InputValue.objects.create(
                user=request.user,
                input_values=input_values_str
            )

            search_result = search_value in input_values

            return render(request, 'khoj_search.html', {'form': form, 'search_result': search_result})

    else:
        form = KhojSearchForm()
    return render(request, 'khoj_search.html', {'form': form})

from django.http import HttpResponse

class GetAllInputValuesView(View):
    def get(self, request):
        user_id = self.request.GET.get('user_id')
        start_datetime = self.request.GET.get('start_datetime')
        end_datetime = self.request.GET.get('end_datetime')

        input_values_queryset = InputValue.objects.filter(
            user_id=user_id,
            timestamp__range=[start_datetime, end_datetime]
        ).order_by('-timestamp')

        payload = [
            {
                "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "input_values": entry.input_values
            }
            for entry in input_values_queryset
        ]

        response_data = {
            "status": "succes",
            "user_id": user_id,
            "payload": payload
        }

        # Manually construct the custom JSON response string
        custom_json_response = (
            '{\n'
            '    “status”: “succes”,\n'
            f'    “user_id” : {response_data["user_id"]},\n'
            '    “payload” : [\n'
        )

        for entry in response_data["payload"]:
            custom_json_response += (
                '         {\n'
                f'              “timestamp” : ”{entry["timestamp"]}”,\n'
                f'              “input_values” : “{entry["input_values"]}”\n'
                '          },\n'
            )

        custom_json_response += (
            '   ]\n'
            '}'
        )

        return HttpResponse(custom_json_response, content_type='application/json')


# This view handles login using Django's built-in authentication views
class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
