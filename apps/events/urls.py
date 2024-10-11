from django.urls import path
from .views import event_list, create_event , update_event , delete_event , event_listfront , event_detail , request_participation  , event_manage_requests , cancel_participation

urlpatterns = [
    path('events/', event_list, name='event_list'),
   path('eventsfront/', event_listfront, name='event_listfront'),
    path('events/create/', create_event, name='create_event'),
    path('events/update/<int:event_id>/', update_event, name='update_event'),  # Update URL
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),  # Delete URL
    path('events/<int:event_id>/', event_detail, name='event_detail'),  # Event detail URL
    path('events/participate/<int:event_id>/', request_participation, name='request_participation'),  # Participation request
    path('events/<int:event_id>/manage_requests/', event_manage_requests, name='event_manage_requests'),
    path('cancel_participation/<int:participation_id>/', cancel_participation, name='cancel_participation'),

]
