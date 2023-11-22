from django.shortcuts import render, redirect, reverse
from urllib.parse import quote, unquote
from django.views import View
from database import utils, models
from accounts.authentication import is_authenticated, get_type
from . import forms
import requests
import datetime
from django.utils.crypto import get_random_string

class TrainSearchView(View):
    template_name = 'trains/search.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            form = forms.TrainSearchForm()
            return render(request, self.template_name, {'form': form, 'type': get_type(request)})

    def post(self, request):
        form = forms.TrainSearchForm(request.POST)
        if form.is_valid():
            From = form.cleaned_data.get('From')
            To = form.cleaned_data.get('To')
            TravelDate = form.cleaned_data.get('TravelDate')
            if From != To and TravelDate >= datetime.date.today():
                query_string = 'From=' + quote(str(form.cleaned_data.get('From'))) + '&To=' + quote(str(form.cleaned_data.get('To'))) + '&TravelDate=' + quote(str(form.cleaned_data.get('TravelDate')))
                return redirect(reverse('trains:Display') + '?' + query_string)
            else:
                return render(request, self.template_name, {'form': form, 'error': '1', 'msg': 'Incorrect Details', 'type': get_type(request)})
        else:
            return render(request, self.template_name, {'form': form, 'error': '1', 'msg': 'Invalid Details', 'type': get_type(request)})

class TrainDisplayView(View):
    template_name = 'trains/display.html'

    def get_trains(self, From, To):
        return utils.get_train_services_city(From, To)

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            trains = self.get_trains(request.GET.get('From'), request.GET.get('To'))
            for train in trains:
                print(train.get('route'))
                train.update({'source': train.get('route')[0]})
                train.update({'destination': train.get('route')[len(train.get('route')) - 1]})
                travel_time = utils.get_travel_time(train.get('timing')[0], train.get('timing')[len(train.get('timing')) - 1])
                train.update({'travel_time': travel_time / 60})

            return render(request, self.template_name, {'trains': trains, 'type': get_type(request)})

class TrainDetailsView(View):
    template_name = 'trains/details.html'

    def get_train_details(self, id):
        return utils.get_train_service_by_id_rep(id)

    def get_rendering_details(self, details, request, Src, Dest):
        From = 'Not Selected'
        To = 'Not Selected'
        start_time = 'NA'
        end_time = 'NA'
        travel_time = 'NA'
        if request.GET.get('From') != None and request.GET.get('To') != None:
            From = request.GET.get('From').upper()
            To = request.GET.get('To').upper()
            idx1 = details.get('route').index(request.GET.get('From').upper())
            idx2 = details.get('route').index(request.GET.get('To').upper())
            start_time = details.get('timing')[idx1]
            end_time = details.get('timing')[idx2]
            travel_time = utils.get_travel_time(start_time, end_time)
            travel_time = int(travel_time) / 60

        return From, To, start_time, end_time, travel_time

    def get(self, request, id):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            details = self.get_train_details(id)
            Src = ''
            Dest = ''
            if request.GET.get('From') != None:
                Src = request.GET.get('From').upper()
            if request.GET.get('To') != None:
                Dest = request.GET.get('To').upper()

            available = details.get('seats') - utils.get_train_bookings_by_train(service_id = id, From = request.GET.get('From'), To = request.GET.get('To'), TravelDate = request.GET.get('TravelDate'))
            form = forms.TrainBookForm(initial = {'available': available, 'TravelDate': request.GET.get('TravelDate'), 'From': Src, 'To': Dest})
            details.update({'source': details.get('route')[0], 'destination': details.get('route')[1]})
            details.update({'combined_list': zip(details.get('route'), details.get('timing'), details.get('boarding_point'))})
            From, To, start_time, end_time, travel_time = self.get_rendering_details(details, request, Src, Dest)
            return render(request, self.template_name, {'from': From, 'to': To, 'start_time': start_time, 'end_time': end_time, 'travel_time': travel_time, 'form': form, 'train': details, 'available': available, 'type': get_type(request)})

    def post(self, request, id):
        form = forms.TrainBookForm(request.POST)
        details = self.get_train_details(id)
        available = int(request.POST.get('available'))
        Src = ''
        Dest = ''
        if request.GET.get('From') != None:
            Src = request.GET.get('From').upper()
        if request.GET.get('To') != None:
            Dest = request.GET.get('To').upper()
        details.update({'source': details.get('route')[0], 'destination': details.get('route')[1]})
        details.update({'combined_list': zip(details.get('route'), details.get('timing'), details.get('boarding_point'))})
        From, To, start_time, end_time, travel_time = self.get_rendering_details(details, request, Src, Dest)
        if form.is_valid():
            seats = int(form.cleaned_data.get('seats'))
            if seats > 0 and seats <= int(available):
                new_id = 'B' + get_random_string(15)
                while(utils.check_booking_id(id = new_id) == False):
                    new_id = 'B' + get_random_string(15)

                bill = int(details.get('price')) * int(form.cleaned_data.get('seats'))
                r = utils.new_train_booking(  id = new_id,
                                            service_id = id,
                                            email = request.session.get('email'),
                                            From = form.cleaned_data.get('From'),
                                            To = form.cleaned_data.get('To'),
                                            TravelDate = form.cleaned_data.get('TravelDate'),
                                            booking_date = datetime.date.today(),
                                            seats = form.cleaned_data.get('seats'),
                                            bill = bill)

                if r == 201:
                    return redirect('booking:Detail', id = new_id)
                else:
                    print(r)
                    return render(request, self.template_name, {'from': From, 'to': To, 'start_time': start_time, 'end_time': end_time, 'travel_time': travel_time / 60, 'available': available, 'form': form, 'error': '1', 'msg': 'Internal Error. Try Again.', 'train': details, 'type': get_type(request)})
            else:
                return render(request, self.template_name, {'from': From, 'to': To, 'start_time': start_time, 'end_time': end_time, 'travel_time': travel_time / 60, 'available': available, 'form': form, 'error': '1', 'msg': 'Enter Valid number of Seats', 'train': details, 'type': get_type(request)})
        else:
            return render(request, self.template_name, {'from': From, 'to': To, 'start_time': start_time, 'end_time': end_time, 'travel_time': travel_time / 60, 'available': available, 'form': form, 'error': '1', 'msg': 'Invalid Submission', 'train': details, 'type': get_type(request)})



# <!-- href="{% url 'trains:Details' id=train.id %}?From={{ request.GET.From|urlencode }}&To={{ request.GET.To|urlencode }}&TravelDate={{ request.GET.TravelDate|urlencode }}" -->
class TrainBookingListView(View):

    template_name = 'trains/bookings.html'

    def check_provider(self, email, id):
        service = models.ServiceMetaData.objects.filter(id = id)
        if not service:
            return False
        else:
            if email in service[0].provider:
                return True
            else:
                return False

    def get_bookings(self, id, date):
        return utils.get_train_booking_by_date(id, date)

    def get(self, request, id):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        if self.check_provider(request.session.get('email'), id) == True:
            bookings = self.get_bookings(id, datetime.date.today())
            form = forms.DateForm(initial = {'date': datetime.date.today})
            return render(request, self.template_name, {'form': form, 'bookings': bookings, 'type': get_type(request)})
        else:
            print('NOT FOUND')

    def post(self, request, id):
        form = forms.DateForm(request.POST)
        if form.is_valid():
            bookings = self.get_bookings(id, form.cleaned_data.get('date'))
            return render(request, self.template_name, {'form': form, 'bookings': bookings, 'type': get_type(request)})
        else:
            return render(request, self.template_name, {'form': form, 'error': '1', 'msg': 'Invalid Submission', 'bookings': bookings, 'type': get_type(request)})
