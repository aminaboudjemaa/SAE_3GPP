import os
import zipfile
import requests
import io


from sae_3gpp_web.settings import EXTRACT_TO
from .ai import get_ai_fields
from .models import Documents

def is_docfile(file:str):
    return file.endswith(".docx") or file.endswith(".doc")

def treat_docs():
    print("started treatment")
    tdocs = Documents.objects.filter(
        content__isnull=True,
    ).all()
    len_tdocs = len(tdocs)
    # for each tdoc
    for i, tdoc in enumerate(tdocs):
        # get the zip file
        res = requests.get(tdoc.zip_link, timeout=10)
        if res.ok:
            # unzip
            with zipfile.ZipFile(io.BytesIO(res.content)) as zip_ref:
                zip_ref.extractall(EXTRACT_TO)
            # get filename inside zip
            files = os.listdir(EXTRACT_TO)
            file = next(
                (f for f in files
                if is_docfile(f)),
                None,
            )
            if file is not None:
                # get ai fields and update in database
                ai_fields = get_ai_fields(EXTRACT_TO+file)
                tdoc.summary = ai_fields["summary"]
                tdoc.topic = ai_fields["topic"]
                tdoc.problem = ai_fields["problem"]
                tdoc.solution = ai_fields["solution"]
                tdoc.content = ai_fields["content"]
                tdoc.save()
                print(f"generated ai fields for {tdoc.tdoc_id}")
                # cleanup zips directory
            for f in files:
                try:
                    os.remove(EXTRACT_TO+f)
                except Exception as e:
                    print(e) 
                    raise e 
        else:
            tdoc.content="Not relevant"
            tdoc.save()         
        print(f"\rProgress {100*i/len_tdocs:.2f}%", end="", flush=True)



from django_q.tasks import async_task, Schedule
from django_q.models import OrmQ

def start_treatment_task():

    # Check if the task is already in queue
    if OrmQ.objects.exists():
        print("Task already queued. Skipping duplicate execution.")
        return False
    
    Schedule.objects.update_or_create(
        name="treat_tdocs",
        defaults={
            "func": "tdocs_interface.treat_tdocs.treat_docs",
            "schedule_type": Schedule.ONCE,
        }
    )
    return True
    
