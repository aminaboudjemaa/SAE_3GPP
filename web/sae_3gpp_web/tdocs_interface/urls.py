


from django.urls import path

from .views import tdoc_list, dashboard, start_doc_treatment, collect_docs, debug, stop_doc_treatment, about, edit_tdoc



urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('d/', debug, name='debug'),
    path('list/', tdoc_list, name='tdoc_list'),
    path('start/', start_doc_treatment, name='start_doc_treatment'),
    path('stop/', stop_doc_treatment, name='stop_doc_treatment'),
    path('about/', about, name='about'),
    path('edit', edit_tdoc, name='edit_tdoc'),
    path('collect/', collect_docs, name='collect_docs'),
]