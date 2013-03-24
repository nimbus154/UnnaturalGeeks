from django.http import HttpResponse

def list(request, job_id):
    return HttpResponse('correspondence list for job %s' % job_id)

def details(request, job_id, correspondence_id):
    return HttpResponse('details for correspondence %s' % correspondence_id) 

'''
GOALS FOR TONIGHT:
    render a correspondence 
        correspondence list on job/id get
        
Need to support the following operations:
    /job/{id}/correspondence
        GET 
            list all correspondences
        POST
            create a new correspondence

    /job/{id}/correspondence/{id}
        PUT
            update a correspondence
        DELETE
            delete a correspondence

    All of this will be included in the job details template.
    
    Template:
        Give it a job. 
            for correspondence in job.correspondence_set
                render single correspondence

        Single template:
            x/pencil in top corner for deleting/updating
            display content
'''
