from django.contrib import admin
from .models import Contact, QuoteRequest, Service, Project, Testimonial
from django.contrib import admin
from .models import SiteSettings, HomePageSection
from django.contrib import admin
from .models import Portfolio, PortfolioImage

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    fields = ('image', 'is_primary', 'caption', 'order')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'completion_date', 'featured')
    list_filter = ('category', 'featured', 'completion_date')
    search_fields = ('title', 'description', 'client')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PortfolioImageInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'google_maps_embed')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin')
        }),
        ('Homepage Content', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_video')
        }),
        ('About Section', {
            'fields': ('about_title', 'about_content', 'about_image')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
    )

    def has_add_permission(self, request):
        # Check if any settings object exists
        if self.model.objects.exists():
            return False
        return True

@admin.register(HomePageSection)
class HomePageSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('featured', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'completion_date', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'featured', 'completion_date')
    search_fields = ('title', 'description', 'client')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'featured')
    list_filter = ('rating', 'featured')
    search_fields = ('name', 'company', 'testimonial')


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('name', 'email', 'project_description')
    readonly_fields = ('created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('name', 'email', 'phone', 'service', 
                                         'project_description', 'budget_range', 
                                         'timeline', 'attachments')
        return self.readonly_fields

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('name', 'email', 'subject', 'message')
        return self.readonly_fields