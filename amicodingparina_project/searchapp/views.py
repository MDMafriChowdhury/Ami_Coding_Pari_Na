from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import views as auth_views
from .forms import KhojSearchForm
from .models import InputValue

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

class GetAllInputValuesView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        start_datetime = request.GET.get('start_datetime')
        end_datetime = request.GET.get('end_datetime')

        input_values = InputValue.objects.filter(
            user_id=user_id,
            timestamp__range=(start_datetime, end_datetime)
        ).values('timestamp', 'input_values')

        response_data = {
            'status': 'success',
            'user_id': user_id,
            'payload': list(input_values)
        }

        return JsonResponse(response_data)

# This view handles login using Django's built-in authentication views
class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
