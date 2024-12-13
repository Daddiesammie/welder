from django.shortcuts import get_object_or_404, render
from .models import Certificate, Portfolio, QuoteRequest, Service, Project, SiteSettings, Testimonial
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm, QuoteRequestForm

import logging
logger = logging.getLogger(__name__)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact = form.save()
                
                # Prepare HTML email
                html_message = render_to_string('emails/contact_notification.html', {
                    'name': contact.name,
                    'email': contact.email,
                    'subject': contact.subject,
                    'message': contact.message,
                })
                plain_message = strip_tags(html_message)
                
                # Send email
                send_mail(
                    subject=f'New Contact Form Submission: {contact.subject}',
                    message=plain_message,
                    html_message=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                )
                
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact_success')
            except Exception as e:
                print("Error:", str(e))
                messages.error(request, 'Error saving your message.')
        else:
            messages.error(request, 'Please check your input.')
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})



def quote_request(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Save to database first
            quote_instance = form.save()
            
            # Prepare email context
            context = {
                'name': quote_instance.name,
                'email': quote_instance.email,
                'phone': quote_instance.phone,
                'service': quote_instance.service,
                'project_description': quote_instance.project_description,
                'budget_range': quote_instance.budget_range,
                'timeline': quote_instance.timeline,
                'tracking_id': quote_instance.tracking_id
            }
            
            # Send email
            try:
                html_message = render_to_string('emails/quote_request.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject='New Quote Request',
                    message=plain_message,
                    html_message=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                )
                messages.success(request, 'Your quote request has been submitted successfully!')
                return render(request, 'main/quote_success.html', {'quote': quote_instance})
            except Exception as e:
                print(f"Email error: {str(e)}")  # For debugging
                messages.warning(request, 'Quote request saved but email notification failed.')
                return render(request, 'main/quote_success.html', {'quote': quote_instance})
    else:
        form = QuoteRequestForm()
    
    return render(request, 'main/quote_request.html', {'form': form})




def home(request):
    featured_services = Service.objects.filter(featured=True)[:3]
    featured_projects = Project.objects.filter(featured=True)[:4]
    testimonials = Testimonial.objects.filter(featured=True)[:3]
    
    context = {
        'featured_services': featured_services,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
    }
    return render(request, 'main/home.html', context)

def services(request):
    featured_services = Service.objects.filter(featured=True)[:3]
    context = {
        'featured_services': featured_services,
    }
    return render(request, 'main/services.html', context)

def portfolio(request):
    category = request.GET.get('category', 'all')
    
    portfolios = Portfolio.objects.prefetch_related('images').all()
    
    if category != 'all':
        portfolios = portfolios.filter(category=category)
    
    categories = Portfolio.CATEGORY_CHOICES
    
    context = {
        'portfolios': portfolios,
        'categories': categories,
        'current_category': category
    }
    return render(request, 'main/portfolio.html', context)

def about(request):
    settings = SiteSettings.objects.first()
    certificates = Certificate.objects.all()
    return render(request, 'main/about.html', {
        'settings': settings,
        'certificates': certificates
    })

def portfolio_detail(request, slug):
    portfolio = get_object_or_404(Portfolio.objects.prefetch_related('images'), slug=slug)
    related_projects = Portfolio.objects.filter(category=portfolio.category).exclude(id=portfolio.id)[:3]
    
    context = {
        'portfolio': portfolio,
        'related_projects': related_projects
    }
    return render(request, 'main/portfolio_detail.html', context)

def quote_success(request):
    return render(request, 'main/quote_success.html')

def contact_success(request):
    return render(request, 'main/contact_success.html')


def track_quote(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        tracking_id = request.POST.get('tracking_id')
        
        quote = QuoteRequest.objects.filter(
            email=email,
            tracking_id=tracking_id
        ).first()
        
        if quote:
            return render(request, 'main/track_result.html', {'quote': quote})
        else:
            messages.error(request, 'No matching quote request found.')
    
    return render(request, 'main/track_quote.html')
