from jobtracker.models import Job, Document, Contact, Correspondence
from django.contrib import admin

class CorrespondenceInline(admin.TabularInline):
    model = Correspondence

class ContactInline(admin.TabularInline):
    model = Contact

class JobAdmin(admin.ModelAdmin):
# display all attributes
# display expandable: contacts, correspondences
    inlines = [
        CorrespondenceInline,
        ContactInline,
    ]

admin.site.register(Job, JobAdmin)
admin.site.register(Document)
