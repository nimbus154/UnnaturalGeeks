from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User # Django's user model

class Job(models.Model):
    job_title   = models.CharField(max_length=75)
    company     = models.CharField(max_length=30)
    post_url    = models.URLField() # default length 200. Long enough?
    applied_on  = models.DateField(verbose_name='date application sent',
                                  blank=True)
    city        = models.CharField(help_text='city where job is located', 
                                   max_length=30)
    state       = models.CharField(help_text='state where job is located', 
                                   max_length=30)
    notes       = models.TextField(blank=True) # lots of notes?
    user        = models.ForeignKey(User)

    def __unicode__(self):
        return '%s at %s (%s, %s)' % (self.job_title, 
                                      self.company, 
                                      self.city, 
                                      self.state)

class JobForm(ModelForm):
    class Meta:
        model   = Job
        #fields = ('contact', 'date', 'message')

class Document(models.Model):
    doc_key     = models.AutoField(primary_key=True)
    doc_ul_date = models.DateTimeField('date uploaded',auto_now_add=True)
    the_doc     = models.FileField(upload_to='docs')
    doc_descr   = models.CharField(max_length=255)
    user_name   = models.ForeignKey(User)
    doc_type    = models.CharField(max_length=20)
    doc_mime    = models.CharField(max_length=255)
    job_ids     = models.ManyToManyField(Job, blank=True,null=True )  #, on_delete=models.SET_NULL

    def __unicode__(self):
        return self.doc_descr

class Document(models.Model):
    ul_date     = models.DateTimeField('date uploaded')
    the_doc     = models.FileField(upload_to='docs')
    descr       = models.CharField(max_length=255)
    DOC_TYPES_CHOICES = (
        ('RS', 'Resume'),
        ('CL', 'Cover Letter'),
        ('FM', 'Form'),
    )
    user_name   = models.ForeignKey(User)
    type        = models.CharField(max_length=2, choices=DOC_TYPES_CHOICES)
    mime        = models.CharField(max_length=255)
    job_id      = models.ForeignKey(Job)        

    def __unicode__(self):
        return '%s: %s' % (type, descr)

class Contact(models.Model):
    name        = models.CharField(max_length=80)
    email       = models.EmailField(blank=True)
    phone       = models.CharField(max_length=20,# to account for foreign #s
                                   blank=True) 
    notes       = models.CharField(max_length=200,
                                  blank=True)
    job         = models.ForeignKey(Job)

    def __unicode__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'notes') 

class Correspondence(models.Model):
    date        = models.DateTimeField()
    message     = models.TextField()
    job         = models.ForeignKey(Job)
    contact     = models.ForeignKey(Contact, blank=True, null=True)
    
    def __unicode__(self):
        return self.message

class CorrespondenceForm(ModelForm):
    class Meta:
        model   = Correspondence
        fields = ('contact', 'date', 'message')
