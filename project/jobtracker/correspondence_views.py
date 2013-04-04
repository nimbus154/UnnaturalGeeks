from django.http import HttpResponse

def main(request, job_id):
    return HttpResponse('correspondence list for job %s' % job_id)

def detail(request, job_id, correspondence_id):
    if(request.method == "POST"): 
        if('delete' in request.POST):
            return HttpResponse('DELETE details for correspondence %s' % correspondence_id) 
        elif('update' in request.POST):
            return HttpResponse('Update details for correspondence %s' % correspondence_id) 
    else:
        return HttpResponse('details for correspondence %s' % correspondence_id) 


'''
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
