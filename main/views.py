from django.shortcuts import get_object_or_404, render
from .models import Portfolio, Service, Project, Testimonial
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import QuoteRequestForm, ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            context = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message']
            }
            
            try:
                send_mail(
                    subject=f'New Contact Message: {contact.subject}',
                    message=render_to_string('emails/contact_message.txt', context),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact_success')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})

def quote_request(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save()
            
            # Send email notification
            context = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'service': form.cleaned_data['service'],
                'project_description': form.cleaned_data['project_description'],
                'budget_range': form.cleaned_data['budget_range'],
                'timeline': form.cleaned_data['timeline']
            }
            
            try:
                send_mail(
                    subject='New Quote Request',
                    message=render_to_string('emails/quote_request.txt', context),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your quote request has been submitted successfully!')
                return redirect('quote_success')
            except Exception as e:
                messages.error(request, 'There was an error submitting your request. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
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
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

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
