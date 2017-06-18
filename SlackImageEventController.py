import greenstalk

def add_to_queue(job_spec):
    stalk = greenstalk.Client()
    jobid = stalk.put(job_spec)
    stalk.close()
    return jobid
