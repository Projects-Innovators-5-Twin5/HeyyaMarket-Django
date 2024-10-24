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
from django.db.models import Count, Sum, Avg , F , Q

from django.db.models.functions import TruncMonth
import stripe
from django.views.decorators.csrf import csrf_exempt
from .pricing_optimization import DynamicPricingRL



stripe.api_key = settings.STRIPE_SECRET

def event_list(request):
    now = timezone.now()
    events = Event.objects.all()
    for event in events:
     if event.status == 'scheduled' and event.end_datetime < now:
            event.status = 'finished'
            event.save()

    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    start_datetime = request.GET.get('start_datetime', '')
    end_datetime = request.GET.get('end_datetime', '')

    # Filter events based on the query
    if query:
        events = events.filter(title__icontains=query)

    # Filter events based on the status
    if status:
        events = events.filter(status=status)

    # Filter events based on start date and end date
    if start_datetime:
        events = events.filter(start_datetime__date__gte=start_datetime)
    if end_datetime:
        events = events.filter(end_datetime__date__lte=end_datetime)

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'event_list_partial.html', {'events': events})

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

            event_type = request.POST.getlist('event_type')
            target_audience = request.POST.getlist('target_audience')
            event_theme = request.POST.getlist('event_theme')
            level = request.POST.getlist('level')

            # Join the selected values into a comma-separated string
            event.event_type = ','.join(event_type)
            event.target_audience = ','.join(target_audience)
            event.event_theme = ','.join(event_theme)
            event.level = ','.join(level)

            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_list')
    else:


        event.event_type = event.event_type.split(',') if event.event_type else []
        event.target_audience = event.target_audience.split(',') if event.target_audience else []
        event.event_theme = event.event_theme.split(',') if event.event_theme else []
        event.level = event.level.split(',') if event.level else []

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
    start_datetime = request.GET.get('start_datetime')
    end_datetime = request.GET.get('end_datetime')


    # Filter events based on the query
    if query:
        events = events.filter(title__icontains=query)  # Adjust filtering as needed

    # Filter events based on the status
    if status:
        events = events.filter(status=status)


    if start_datetime:
        events = events.filter(start_datetime__gte=start_datetime)  # Start date
    if end_datetime:
        events = events.filter(end_datetime__lte=end_datetime)  # End date


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
    layout_context['stripe_public_key'] = settings.STRIPE_KEY
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
    confirmed_count = participants.count()  # Number of confirmed participants
    available_slots = event.available_slots  # Available slots
    total_capacity = confirmed_count + available_slots  # Total capacity for attendance
    attendance_percentage = (confirmed_count / total_capacity * 100) if total_capacity > 0 else 0  # Calculate percentage
    layout_context['attendance_percentage'] = attendance_percentage  # Pass the attendance percentage to the template
    layout_context['rating_options'] = range(1, 6)

    if event.status == 'finished':
        average_rating = participants.aggregate(Avg('rating'))['rating__avg']
        layout_context['average_rating'] = average_rating if average_rating is not None else None  # Default to 0 if no ratings
    else:
        layout_context['average_rating'] = None

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

    if request.method == "POST":
        if request.user.role == 'VENDEUR':
            # Check if the user already has a participation request for this event
            participation = Participation.objects.filter(event=event, user=request.user).first()

            if participation:
                if participation.status == 'cancelled':
                    # Reactivate participation request
                    participation.status = 'pending'
                    participation.save()
                    messages.success(request, "Participation request sent successfully.")
                else:
                    messages.info(request, "You have already requested participation.")
                    return redirect('event_detail', event_id=event.id)  # Redirect after message
            else:
                # Create a new participation request
                participation = Participation(event=event, user=request.user, status='pending')
                participation.save()  # Save the new participation

            if event.price > 0:
                # Return a response to open the payment modal
                return JsonResponse({
                    'status': 'modal',
                    'message': "Open payment modal",
                    'participation_id': participation.id  # Send back the participation ID
                })
            else:
                # Accept participation directly if price is 0
                participation.status = 'pending'
                participation.save()
                messages.success(request, "Participation request sent successfully and accepted.")
                return redirect('event_detail', event_id=event.id)
        else:
            messages.error(request, "You do not have permission to request participation.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect('event_detail', event_id=event.id)


@csrf_exempt
def process_payment(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)

        # Get the payment method ID from the request body
        data = json.loads(request.body)
        payment_method_id = data.get("payment_method_id")
        participation_id = data.get("participation_id")  # Get the participation ID

        if not payment_method_id:
            return JsonResponse({'error': 'Payment method ID is required'}, status=400)

        try:
            # Create a Payment Intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(event.price * 100),  # Amount in cents
                currency='usd',
                payment_method=payment_method_id,
                automatic_payment_methods={
                    'enabled': True,
                }
            )

            # Update participation status to accepted
            event.available_slots -= 1
            participation = get_object_or_404(Participation, id=participation_id)
            participation.status = 'confirmed'


            participation.save()
            event.save()
            # Return the client_secret
            return JsonResponse({'client_secret': payment_intent['client_secret']})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def dynamic_pricing(request, event_id):
    # Fetch the event object
    event = get_object_or_404(Event, id=event_id)

    # Get the number of confirmed participants (for calculating demand)
    confirmed_participants = Participation.objects.filter(event=event, status='confirmed').count()

    # Demand over time simulation (this could be replaced by real-time data)
    demand_over_time = [confirmed_participants] * 10  # For simplicity, using the same demand repeatedly

    # Initialize the pricing model
    pricing_model = DynamicPricingRL(event)

    # Run the pricing simulation
    optimized_price = pricing_model.run_simulation(demand_over_time)

    # Update the event's dynamic price in the database
    event.dynamic_price = optimized_price
    event.save()

    return JsonResponse({
        'message': 'Dynamic pricing updated successfully.',
        'optimized_price': optimized_price
    })


def payment_success(request):
    event_id = request.GET.get('event_id')
    if event_id:
        event = get_object_or_404(Event, id=event_id)

        # Create the participation record and set status to 'accepted'
        participation = Participation.objects.create(event=event, user=request.user, status='confirmed')
        participation.save()
        messages.success(request, "Payment successful! Your participation is confirmed.")
        print("Payment successful, participation status set to accepted.")
    else:
        messages.error(request, "No event ID provided.")

    # Redirect to the event detail page
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



def events_analytics(request):
    layout_context = TemplateLayout.init(request, {})
    layout_context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", layout_context)

    now = timezone.now()
    current_year = now.year

    # Total number of events
    total_events = Event.objects.count()
    active_events = Event.objects.filter(status='scheduled').count()
    finished_events = Event.objects.filter(status='finished').count()
    cancelled_events = Event.objects.filter(status='cancelled').count()

    # Participation metrics
    total_participations = Participation.objects.count()
    confirmed_participations = Participation.objects.filter(status='confirmed').count()
    pending_participations = Participation.objects.filter(status='pending').count()
    refused_participations = Participation.objects.filter(status='refused').count()
    average_rating = Participation.objects.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg'] or 0

    # Top event of the month
    current_month = now.month
    top_event = Event.objects.filter(
        available_slots=0,
        status='finished',
        end_datetime__month=current_month,
        end_datetime__year=current_year
    ).annotate(participant_count=Count('participation')).order_by('-participant_count').first()

    if top_event:
        top_event_title = top_event.title
        top_event_type = top_event.event_type
        top_event_participants = top_event.participant_count
        top_event_rating = Participation.objects.filter(event=top_event).aggregate(Avg('rating'))['rating__avg'] or 0
    else:
        top_event_title = 'No event found'
        top_event_type = 'N/A'
        top_event_participants = 0
        top_event_rating = 0

    total_participants = Participation.objects.filter(status='confirmed').count()
    total_available_slots = Event.objects.filter(status='scheduled').aggregate(total=Sum('available_slots'))['total'] or 0

    monthly_event_data = (
     Event.objects.filter(start_datetime__year=current_year)  # Ensure events are from the current year
     .annotate(month=TruncMonth('start_datetime'))  # Group by month
     .values('month')
     .annotate(event_count=Count('id'))  # Count events per month
     .annotate(total_income=Sum('participation__event__price', filter=Q(participation__status='confirmed')))  # Calculate income from confirmed participations
     .filter(start_datetime__year=current_year)  # Filter only current year's events
     .order_by('month')
    )

    # Prepare data for the chart
    months = []
    event_counts = []
    income_counts = []

    for month in range(1, 13):
        month_name = datetime(current_year, month, 1).strftime('%B %Y')
        months.append(month_name)

        # Filter monthly data for the current month
        current_month_data = next((data for data in monthly_event_data if data['month'].month == month), None)

        if current_month_data:
            event_count = current_month_data['event_count']
            total_income = current_month_data['total_income'] or 0
            total_income /= 1000  # Divide by 1000 to adjust income to the correct currency format
        else:
            event_count = 0
            total_income = 0

        event_counts.append(event_count)
        income_counts.append(total_income)

    # Adding data to context
    layout_context.update({
        'total_events': total_events,
        'active_events': active_events,
        'finished_events': finished_events,
        'cancelled_events': cancelled_events,
        'average_rating': round(average_rating, 2),
        'top_event_title': top_event_title,
        'top_event_type': top_event_type,
        'top_event_participants': top_event_participants,
        'top_event_rating': round(top_event_rating, 2),
        'total_participants': total_participants,
        'total_available_slots': total_available_slots,
        'months': months,
        'event_counts': event_counts,
        'income_counts': income_counts,
    })

    return render(request, 'events_analytics.html', layout_context)
