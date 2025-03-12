import json

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
    tdocs_dicts = [
        {        
            'meeting': doc.meeting,
            'zip_link': doc.zip_link,
            'tdoc_id': doc.tdoc_id,
            'title': doc.title,
            'type': doc.type,
            'source': doc.source,
            'content': doc.content,
            'topic': doc.topic,
            'summary': doc.summary,
            'problem': doc.problem,
            'solution': doc.solution,
        }
        for doc in tdocs
    ] 
    return render(request, 'tableau.html', {'docs':tdocs_dicts})

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

def stop_doc_treatment(request):
    OrmQ.objects.all().delete()
    return JsonResponse({"message":"Task stopped"})

def edit_tdoc(request):
    if request.method == "POST":
        try:
            print(request.body)
            data = json.loads(request.body)  # Parse JSON request body
            tdoc_id = data.get("tdoc_id")
            doc = Documents.objects.get(tdoc_id=tdoc_id)
            topic = data.get("topic", doc.topic)
            content = data.get("content", doc.content)
            summary = data.get("summary", doc.summary)
            problem = data.get("problem", doc.problem)
            solution = data.get("solution", doc.solution)
            doc.topic = topic
            doc.content = content
            doc.summary = summary
            doc.problem = problem
            doc.solution = solution
            doc.save()

            return JsonResponse({"message": "document updated", "tdoc_id": doc.tdoc_id}, status=200)

        except Documents.DoesNotExist:
            return JsonResponse({"error": "document not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=400)

def about(request):
    return render(request, "about.html")

def collect_docs(request):
    collect()


def debug(request):
    return render(request, "d.html")
    return JsonResponse(list(x.q_options() for x in OrmQ.objects.all()), safe=False)
    