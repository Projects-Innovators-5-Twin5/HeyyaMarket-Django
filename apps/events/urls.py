from django.urls import path
from .views import event_list, create_event , update_event , delete_event , event_listfront , event_detail , request_participation  , event_manage_requests , cancel_participation , calendar_view , calendar_update_event

urlpatterns = [
    path('events/', event_list, name='event_list'),
    path('events/calendar/', calendar_view, name='calendar_view'),  
    path('events/calendar/update/<int:event_id>/', calendar_update_event, name='calendar_update_event'),  

    path('eventsfront/', event_listfront, name='event_listfront'),
    path('events/create/', create_event, name='create_event'),
    path('events/update/<int:event_id>/', update_event, name='update_event'),  
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'), 
    path('events/<int:event_id>/', event_detail, name='event_detail'),  
    path('events/participate/<int:event_id>/', request_participation, name='request_participation'),  
    path('events/<int:event_id>/manage_requests/', event_manage_requests, name='event_manage_requests'),
    path('cancel_participation/<int:participation_id>/', cancel_participation, name='cancel_participation'),

]
