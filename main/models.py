from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Service(models.Model):
    ICON_CHOICES = [
        ('fa-bolt', 'Bolt'),
        ('fa-fire', 'Fire'),
        ('fa-cog', 'Cog'),
        ('fa-tools', 'Tools'),
        ('fa-wrench', 'Wrench'),
        ('fa-hammer', 'Hammer'),
        ('fa-industry', 'Industry'),
        ('fa-hard-hat', 'Hard Hat'),
        ('fa-truck', 'Truck'),
        ('fa-ruler', 'Ruler'),
        ('fa-drafting-compass', 'Compass'),
        ('fa-layer-group', 'Layers'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    image = models.ImageField(upload_to='services/images/')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='portfolio/')
    client = models.CharField(max_length=200)
    completion_date = models.DateField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    testimonial = RichTextField()
    image = models.ImageField(upload_to='testimonials/')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company}"


from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache

class SiteSettings(models.Model):
    # Basic Info
    site_name = models.CharField(max_length=100)
    site_logo = models.ImageField(upload_to='site/')
    favicon = models.ImageField(upload_to='site/')
    
    # Contact Info
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    google_maps_embed = models.TextField(help_text="Paste your Google Maps embed code here")
    
    # Social Media
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    # Homepage Content
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.CharField(max_length=200)
    hero_video = models.FileField(upload_to='site/videos/', blank=True)
    
    # About Section
    about_title = models.CharField(max_length=200)
    about_content = RichTextField()
    about_image = models.ImageField(upload_to='site/')
    
    # Footer
    footer_text = RichTextField()
    
    # SEO
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache when settings are updated
        cache.clear()

    def __str__(self):
        return self.site_name

class HomePageSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='sections/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('industrial', 'Industrial'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('artistic', 'Artistic'),
        ('structural', 'Structural'),
        ('custom', 'Custom Projects')
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    client = models.CharField(max_length=200)
    completion_date = models.DateField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.portfolio.title} - Image {self.order}"
    

class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('in_progress', 'In Progress'),
        ('approved', 'Quote Approved'),
        ('declined', 'Quote Declined'),
        ('completed', 'Project Completed')
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    project_description = models.TextField()
    budget_range = models.CharField(max_length=50)
    timeline = models.CharField(max_length=100)
    attachments = models.FileField(upload_to='quotes/attachments/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_id = models.CharField(max_length=12, unique=True, editable=False, null=True)
    status_updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = f'WTP-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Quote Request from {self.name}"

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.name}: {self.subject}"
    
class Certificate(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='certificates/')
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name