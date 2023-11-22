from django.contrib import admin
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [

    path('user/list', views.UserList.as_view()),
    path('user/get', views.GetUser.as_view()),
    path('user/insert', views.InsertUser.as_view()),
    path('user/update', views.UpdateUser.as_view()),
    path('bus/list', views.BusServiceList.as_view()),
    path('bus/insert', views.NewBusService.as_view()),
    path('bus/delete', views.DeleteBusService.as_view()),
    path('bus/list/email', views.BusServiceListEmail.as_view()),
    path('bus/update', views.UpdateBusService.as_view()),
    path('bus/get', views.GetBusService.as_view()),
    path('hotels/list', views.HotelServiceList.as_view()),
    path('hotels/insert', views.NewHotelService.as_view()),
    path('hotels/update', views.UpdateHotelService.as_view()),
    path('hotels/get', views.GetHotelService.as_view()),
    path('hotels/delete', views.DeleteHotelService.as_view()),
    path('hotels/list/email', views.HotelServiceListEmail.as_view()),
    path('hotels/list/city', views.GetHotelByCity.as_view()),
    path('bookings/hotel/list', views.HotelBookingList.as_view()),
    path('bookings/hotel/new', views.NewHotelBooking.as_view()),
    path('bookings/hotel/get', views.HotelBookingByHotel.as_view()),
    path('bookings/hotel/user/<str:email>', views.GetHotelBookingByUser.as_view()),
    path('bookings/hotel/id/<slug:id>', views.GetHotelBookingById.as_view()),
    path('bookings/hotel/delete', views.DeleteHotelBooking.as_view()),
    path('bookings/hotel/date', views.HotelBookingsByDate.as_view()),
    path('status', views.StatusView.as_view()),

    path('bus/list/city', views.GetBusByCity.as_view()),
    path('bookings/bus/get', views.BusBookingByBus.as_view()),
    path('bookings/bus/new', views.NewBusBooking.as_view()),
    path('bookings/bus/id/<slug:id>', views.GetBusBookingById.as_view()),
    path('bookings/bus/delete', views.DeleteBusBooking.as_view()),
    path('bookings/bus/user/<str:email>', views.GetBusBookingByUser.as_view()),
    path('bookings/bus/date', views.BusBookingsByDate.as_view()),
    
    path('train/list', views.TrainServiceList.as_view()),
    path('train/insert', views.NewTrainService.as_view()),
    path('train/delete', views.DeleteTrainService.as_view()),
    path('train/list/email', views.TrainServiceListEmail.as_view()),
    path('train/update', views.UpdateTrainService.as_view()),
    path('train/get', views.GetTrainService.as_view()),
    path('train/list/city', views.GetTrainByCity.as_view()),
    path('bookings/train/get', views.TrainBookingByTrain.as_view()),
    path('bookings/train/new', views.NewTrainBooking.as_view()),
    path('bookings/train/id/<slug:id>', views.GetTrainBookingById.as_view()),
    path('bookings/train/delete', views.DeleteTrainBooking.as_view()),
    path('bookings/train/user/<str:email>', views.GetTrainBookingByUser.as_view()),
    path('bookings/train/date', views.TrainBookingsByDate.as_view()),

]
