from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from django_q.models import OrmQ


from .models import Documents
from .treat_tdocs import start_treatment_task
from .collect import collect

EXCLUDED_MEETINGS = [
   f"TSGS2_{i}" for i in range(100)
]+[
    "Electronic",
    "Electronic ",
    "tdocs"
]

def tdoc_list(request):
    tdocs = Documents.objects.filter(topic__isnull=False).all()
    # for i, tdoc in enumerate(tdocs):
    #     tdoc.meeting = tdoc.meeting_
    #     tdoc.save()
    #     if i%1000:
    #         print(f'\r{100*i/len(tdocs)}%% {tdoc.meeting_}', flush=False)
    return render(request, 'tableau.html', {'docs': tdocs})

def dashboard(request):
    tdocs_treated = Documents.objects.filter(topic__isnull=False).count()
    tdocs_all = Documents.objects.count()
    untreated = tdocs_all - tdocs_treated
    meetings = Documents.objects.exclude(meeting__in=EXCLUDED_MEETINGS).values("meeting").annotate(total=Count("tdoc_id"))
    labels = [meet["meeting"]  for meet in meetings if meet["meeting"]  not in (None, "TSGS2_04", "TSGS2_09", "TSGS2_10", "TSGS2_11")]
    data = [meet["total"] for meet in meetings if  meet["meeting"]  not in (None, "TSGS2_04", "TSGS2_09", "TSGS2_10", "TSGS2_11")]
    has_tasks = OrmQ.objects.exists()
    return render(
        request,
        'dashboard.html',
        {
            'nb_total': tdocs_all,
            'nb_treated': tdocs_treated,
            'nb_untreated':untreated,
            'meetings':meetings,
            'labels': labels,
            'has_tasks': has_tasks,
            'data': data,
        }
    )


def start_doc_treatment(request):
    res = start_treatment_task()
    if res:
        return JsonResponse({"message":"Task started"})
    else:
        return JsonResponse({"message":"Task already started"})

    

def collect_docs(request):
    collect()


def debug(request):
    return JsonResponse(list(x.q_options() for x in OrmQ.objects.all()), safe=False)
    