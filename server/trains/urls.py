from django.urls import path
from . import views

app_name = 'trains'

urlpatterns = [

    path('trains', views.TrainSearchView.as_view(), name = 'Search'),
    path('trains/list', views.TrainDisplayView.as_view(), name = 'Display'),
    path('trains/view/<slug:id>', views.TrainDetailsView.as_view(), name = 'Details'),
    path('trains/bookings/<slug:id>', views.TrainBookingListView.as_view(), name = 'Bookings'),

]
