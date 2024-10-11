from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participation
from .forms import EventForm
from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

def event_list(request):
    events = Event.objects.all()  # Fetch all events

    # Initialize the layout context
    layout_context = TemplateLayout.init(request, {})  
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)  # Set the layout path

    # Add events to the layout context
    layout_context['events'] = events

    return render(request, 'event_list.html', layout_context)  # Render with layout context



def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Include request.FILES here
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('event_list')
    else:
        form = EventForm()
    
    layout_context = TemplateLayout.init(request, {})
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)
    layout_context['form'] = form

    return render(request, 'create_event.html', layout_context)

def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)  # Include request.FILES here
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    layout_context = TemplateLayout.init(request, {})
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)
    layout_context['form'] = form

    return render(request, 'update_event.html', layout_context)




def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('event_list')  # Redirect to the event list after deletion
    return redirect('event_list')  # Redirect if the request method is not POST



def event_listfront(request):
    events = Event.objects.all()  # Fetch all events

    # Initialize the layout context
    layout_context = TemplateLayout.init(request, {})  
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_user.html", layout_context)  # Set the layout path

    # Add events to the layout context
    layout_context['events'] = events

    return render(request, 'event_listfront.html', layout_context)  # Render with layout context

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    layout_context = TemplateLayout.init(request, {})
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_user.html", layout_context)
    layout_context['event'] = event  # Pass the event to the template

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_is_vendeur = request.user.role == 'VENDEUR'
        
        # Get the user's participation record
        user_participation = Participation.objects.filter(event=event, user=request.user).first()
        
        # Determine if the user has requested participation and the status
        has_requested = user_participation is not None
        participation_status = user_participation.status if has_requested else None
        
    else:
        user_is_vendeur = False
        has_requested = False
        participation_status = None

    layout_context['user_is_vendeur'] = user_is_vendeur
    layout_context['has_requested'] = has_requested
    layout_context['participation_status'] = participation_status  # Pass participation status to template

    # Get confirmed participants for the event
    participants = Participation.objects.filter(event=event, status='confirmed')  # Only confirmed participants
    layout_context['participants'] = participants  # Add participants to the context

    return render(request, 'event_detail.html', layout_context)  # Render the detail template



def request_participation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Log the user role and authentication status
    print(f"User Role: {request.user.role}, User Authenticated: {request.user.is_authenticated}")

    if request.method == "POST":
        # Ensure the user is a vendeur
        if request.user.role == 'VENDEUR':
            print("User is vendeur.")
            # Try to fetch the user's participation record for the event
            participation = Participation.objects.filter(event=event, user=request.user).first()

            if participation:
                if participation.status == 'cancelled':
                    # Update status to pending if it was cancelled
                    participation.status = 'pending'
                    participation.save()
                    messages.success(request, "Participation request sent successfully.")
                    print("Participation status updated to pending.")
                else:
                    messages.info(request, "You have already requested participation.")
                    print("Participation already exists with status: ", participation.status)
            else:
                # Create a new participation record if it does not exist
                participation = Participation(event=event, user=request.user, status='pending')
                participation.save()
                messages.success(request, "Participation request sent successfully.")
                print("New participation created.")

        else:
            messages.error(request, "You do not have permission to request participation.")
            print("User does not have permission.")

    else:
        messages.error(request, "Invalid request method.")
        print("Invalid request method.")

    return redirect('event_detail', event_id=event.id)





def event_manage_requests(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Fetch participation requests and all participants
    participation_status = request.GET.get('status', 'all')  # Get status filter from request

    # Filter participation requests based on status
    if participation_status == 'pending':
        participations = Participation.objects.filter(event=event, status='pending')
    elif participation_status == 'confirmed':
        participations = Participation.objects.filter(event=event, status='confirmed')
    elif participation_status == 'rejected':
        participations = Participation.objects.filter(event=event, status='rejected')
    elif participation_status == 'cancelled':
        participations = Participation.objects.filter(event=event, status='cancelled')
    else:
        participations = Participation.objects.filter(event=event)  # Get all

    # Handle accept/reject participation requests
    if request.method == 'POST':
        action = request.POST.get('action')
        participation_id = request.POST.get('participation_id')
        participation = get_object_or_404(Participation, id=participation_id)

        if action == 'approve':
            if event.available_slots > 0:  # Ensure there are available slots
                participation.status = 'confirmed'
                event.available_slots -= 1  # Decrease the number of available slots
                messages.success(request, f"Participation request from {participation.user.username} approved.")
                event.save()  # Save the updated event
            else:
                messages.error(request, "No available slots for this event.")
        elif action == 'reject':
            participation.status = 'rejected'
            messages.success(request, f"Participation request from {participation.user.username} rejected.")


        elif action == 'cancel':
            if participation.status == 'confirmed':
                # Increase the available slots back if the participation was confirmed
                event.available_slots += 1
                messages.success(request, f"Participation request from {participation.user.username} has been cancelled.")
            participation.status = 'cancelled'  # Set participation status to cancelled

      
      
      
        participation.save()  # Save the participation status change
        return redirect('event_manage_requests', event_id=event_id)

    # Initialize layout context
    layout_context = TemplateLayout.init(request, {})
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)
    layout_context['event'] = event
    layout_context['participations'] = participations  # Use consolidated list

    return render(request, 'event_manage_requests.html', layout_context)


def cancel_participation(request, participation_id):
    participation = get_object_or_404(Participation, id=participation_id)

    # Check if the user is the one who requested the participation
    if participation.user == request.user:
        # Increase available slots in the event
        event = participation.event
        event.available_slots += 1  # Increase the number of available slots
        event.save()  # Save the updated event

        participation.status = 'cancelled'  # Set participation status to cancelled
        participation.save()  # Save the participation status change
        messages.success(request, f"Participation from {participation.user.username} has been cancelled.")
    else:
        messages.error(request, "You are not authorized to cancel this participation.")

    return redirect('event_detail', event_id=participation.event.id)
