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
from django.db.models import Q
from django.http import JsonResponse
import json
from datetime import datetime, time, date , timedelta 
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils import timezone  
from .nlp_utils import generate_event_description  
from .nlp_utils1 import generate_event_descriptioncohere  
from django.core.files.base import ContentFile
import requests
import base64
from .imageutils import generate_event_image
from .descriptionutils import generate_event_descriptionhug
from django.conf import settings  
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


generate_event_descriptionhug
def event_list(request):
    now = timezone.now()
    events = Event.objects.all()  

    for event in events:
     if event.status == 'scheduled' and event.end_datetime < now:
            event.status = 'finished'
            event.save()


    # Initialize the layout context
    layout_context = TemplateLayout.init(request, {})  
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)  # Set the layout path

    # Add events to the layout context
    layout_context['events'] = events

    return render(request, 'event_list.html', layout_context)  # Render with layout context

def calendar_view(request):
    events = Event.objects.all()  # Fetch all events

    layout_context = TemplateLayout.init(request, {})
    
    # Check if the user is authenticated and has the admin role
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)
        else:
            layout_context['layout_path'] = TemplateHelper.set_layout("layout_user.html", layout_context)
    else:
        layout_context['layout_path'] = TemplateHelper.set_layout("layout_user.html", layout_context)

    layout_context['events'] = events

    return render(request, 'calendar_view.html', layout_context)


def calendar_update_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        data = json.loads(request.body)
        start_time = event.start_datetime.time() 
        end_time = event.end_datetime.time()     

        start_datetime = timezone.datetime.fromisoformat(data.get('start'))
        end_datetime = timezone.datetime.fromisoformat(data.get('end'))

        event.start_datetime = timezone.make_aware(datetime.combine(start_datetime.date(), start_time))
        event.end_datetime = timezone.make_aware(datetime.combine(end_datetime.date(), end_time))

        if event.end_datetime <= event.start_datetime:
            event.end_datetime = event.start_datetime + timedelta(days=1)  

        event.save()

        return JsonResponse({'success': True, 'event_id': event.id})

    return JsonResponse({'success': False}, status=400)

def create_event(request):
    start_date = request.GET.get('start_date')  
    initial_data = {}

    if start_date:
        parsed_start_date = parse_datetime(start_date)  
        if parsed_start_date:  
            initial_data['start_datetime'] = parsed_start_date.strftime('%Y-%m-%dT%H:%M')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.event_type = ','.join(form.cleaned_data['event_type'])
            event.target_audience = ','.join(form.cleaned_data['target_audience'])
            event.event_theme = ','.join(form.cleaned_data['event_theme'])
            event.level = ','.join(form.cleaned_data['level'])

            # Auto-generate description if not provided
            if not event.description:
                event.description = generate_event_descriptioncohere(
                    event.title, event.start_datetime, event.end_datetime, event.location, event.available_slots,event.event_type,event.target_audience,event.event_theme,event.level
                )

            if not event.image:
                # Generate the image and get just the image filename
                image_filename = generate_event_image(
                    title=event.title,
                    description=event.description,
                    location=event.location,
                    start_datetime=event.start_datetime,
                    end_datetime=event.end_datetime,
                    available_slots=event.available_slots,
                    event_type = event.event_type,
                    target_audience = event.target_audience,
                    event_theme = event.event_theme,
                    level= event.level 

                )

                event.image = f'events/{image_filename}'  
            
            event.save()
            messages.success(request, "Event created successfully.")
            return redirect('event_list')
    else:
        form = EventForm(initial=initial_data)

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
    # Start with all events
    events = Event.objects.all()

    # Get the search query and status from the request
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    # Filter events based on the query
    if query:
        events = events.filter(title__icontains=query)  # Adjust filtering as needed

    # Filter events based on the status
    if status:
        events = events.filter(status=status)

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'event_listfront_partial.html', {'events': events})

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
        layout_context['participation'] = user_participation
    
    else:
        user_is_vendeur = False
        has_requested = False
        participation_status = None
        layout_context['participation'] = None 
    layout_context['user_is_vendeur'] = user_is_vendeur
    layout_context['has_requested'] = has_requested
    layout_context['participation_status'] = participation_status  # Pass participation status to template

    # Get confirmed participants for the event
    participants = Participation.objects.filter(event=event, status='confirmed')  # Only confirmed participants
    layout_context['participants'] = participants  # Add participants to the context
    layout_context['rating_options'] = range(1, 6)  
    # Handle feedback submission
    if request.method == "POST":
        if has_requested and participation_status == 'confirmed' and event.status == 'finished':
            feedback = request.POST.get("feedback")
            rating = request.POST.get("rating")

            if user_participation:
                user_participation.feedback = feedback
                user_participation.rating = rating
                user_participation.save()

                messages.success(request, 'Your feedback has been submitted successfully!')
                return redirect('event_detail', event_id=event.id)

    return render(request, 'event_detail.html', layout_context)  # Render the detail template


def request_participation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    print(f"User Role: {request.user.role}, User Authenticated: {request.user.is_authenticated}")

    if request.method == "POST":
        if request.user.role == 'VENDEUR':
            print("User is vendeur.")
            participation = Participation.objects.filter(event=event, user=request.user).first()

            if participation:
                if participation.status == 'cancelled':
                    participation.status = 'pending'
                    participation.save()
                    messages.success(request, "Participation request sent successfully.")
                    print("Participation status updated to pending.")
                else:
                    messages.info(request, "You have already requested participation.")
                    print("Participation already exists with status: ", participation.status)
            else:
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

    participation_status = request.GET.get('status', 'all')  # Get status filter from request

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

    if request.method == 'POST':
        action = request.POST.get('action')
        participation_id = request.POST.get('participation_id')
        participation = get_object_or_404(Participation, id=participation_id)

        if action == 'approve':
            if event.available_slots > 0:  
                participation.status = 'confirmed'
                event.available_slots -= 1  
                messages.success(request, f"Participation request from {participation.user.username} approved.")
                event.save()  
                # Render the email template
                html_content = render_to_string('emails/eventparticipation_confirmation.html', {
                    'user': participation.user,
                    'event': event,
                })
                text_content = strip_tags(html_content)  # Fallback plain text content

                # Create an email message object with both HTML and plain text
                email = EmailMultiAlternatives(
                    subject='Participation Confirmation',
                    body=text_content,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[participation.user.email]
                )

                # Attach the HTML content
                email.attach_alternative(html_content, "text/html")
                email.send()  # Send the email
            else:
                messages.error(request, "No available slots for this event.")
        elif action == 'reject':
            participation.status = 'rejected'
            messages.success(request, f"Participation request from {participation.user.username} rejected.")


        elif action == 'cancel':
            if participation.status == 'confirmed':
                event.available_slots += 1
                messages.success(request, f"Participation request from {participation.user.username} has been cancelled.")
            participation.status = 'cancelled'  

      
      
      
        participation.save()  
        return redirect('event_manage_requests', event_id=event_id)

    # Initialize layout context
    layout_context = TemplateLayout.init(request, {})
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)
    layout_context['event'] = event
    layout_context['participations'] = participations 

    return render(request, 'event_manage_requests.html', layout_context)


def cancel_participation(request, participation_id):
    participation = get_object_or_404(Participation, id=participation_id)

    if participation.user == request.user:
        event = participation.event
        event.available_slots += 1  
        event.save()  

        participation.status = 'cancelled' 
        participation.save()  
        messages.success(request, f"Participation from {participation.user.username} has been cancelled.")
    else:
        messages.error(request, "You are not authorized to cancel this participation.")

    return redirect('event_detail', event_id=participation.event.id)
