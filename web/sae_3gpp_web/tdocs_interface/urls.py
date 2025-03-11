


from django.urls import path

from .views import tdoc_list, dashboard, start_doc_treatment, collect_docs, debug



urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('d/', debug, name='debug'),
    path('list/', tdoc_list, name='tdoc_list'),
    path('treat/', start_doc_treatment, name='start_doc_treatment'),
    path('collect/', collect_docs, name='collect_docs'),
]