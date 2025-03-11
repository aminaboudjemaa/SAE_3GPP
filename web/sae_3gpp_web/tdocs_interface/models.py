from django.db import models

import pandas as pd
import re


class Documents(models.Model):
    tdoc_id = models.CharField(primary_key=True, max_length=500)
    title = models.CharField(blank=True, null=True, max_length=500)
    source = models.CharField(blank=True, null=True, max_length=500)
    contact = models.CharField(blank=True, null=True, max_length=500)
    contact_id = models.CharField(blank=True, null=True, max_length=500)
    type = models.CharField(blank=True, null=True, max_length=500)
    doc_for = models.CharField(blank=True, null=True, max_length=500)
    abstract = models.CharField(blank=True, null=True, max_length=500)
    secretary_remarks = models.CharField(blank=True, null=True, max_length=500)
    agenda_item_sort_order = models.CharField(blank=True, null=True, max_length=500)
    agenda_item = models.CharField(blank=True, null=True, max_length=500)
    agenda_item_description = models.CharField(blank=True, null=True, max_length=500)
    tdoc_sort_order_within_agenda_item = models.CharField(blank=True, null=True, max_length=500)
    tdoc_status = models.CharField(blank=True, null=True, max_length=500)
    reservation_date = models.CharField(blank=True, null=True, max_length=500)
    uploaded = models.CharField(blank=True, null=True, max_length=500)
    is_revision_of = models.CharField(blank=True, null=True, max_length=500)
    revised_to = models.CharField(blank=True, null=True, max_length=500)
    release = models.CharField(blank=True, null=True, max_length=500)
    spec = models.CharField(blank=True, null=True, max_length=500)
    version = models.CharField(blank=True, null=True, max_length=500)
    related_wis = models.CharField(blank=True, null=True, max_length=500)
    cr = models.CharField(blank=True, null=True, max_length=500)
    cr_revision = models.CharField(blank=True, null=True, max_length=500)
    cr_category = models.CharField(blank=True, null=True, max_length=500)
    tsg_cr_pack = models.CharField(blank=True, null=True, max_length=500)
    reply_to = models.CharField(blank=True, null=True, max_length=500)
    to = models.CharField(blank=True, null=True, max_length=500)
    cc = models.CharField(blank=True, null=True, max_length=500)
    original_ls = models.CharField(blank=True, null=True, max_length=500)
    reply_in = models.CharField(blank=True, null=True, max_length=500)
    
    url = models.CharField(blank=True, null=True, max_length=500)
    content = models.CharField(blank=True, null=True, max_length=500)
    summary = models.CharField(blank=True, null=True, max_length=500)
    topic = models.CharField(blank=True, null=True, max_length=500)
    problem = models.CharField(blank=True, null=True, max_length=500)
    solution = models.CharField(blank=True, null=True, max_length=500)
    meeting = models.CharField(blank=True, null=True, max_length=500)

    class Meta:
        db_table = 'documents'


    @property
    def zip_link(self):
        return '/'.join(self.url.split('/')[:-1]+[self.tdoc_id+".zip"])
    
    @property
    def meeting_(self):
        full_name = self.url.split("/")[-3]
        splitted = full_name.split('_')
        if len(splitted)>=3:
            return re.sub(r"[\d-]", "", " ".join(splitted[2:]))
        
        return full_name


    def __init__(self,df:pd.DataFrame, url:str):
        self.url=url
        self.tdoc_id = str(df['TDoc'])
        self.title = str(df['Title'])
        self.source = str(df['Source'])
        self.contact = str(df['Contact'])
        self.contact_id = str(df['Contact ID'])
        self.type = str(df['Type'])
        self.doc_for = str(df['For'])
        self.abstract = str(df['Abstract'])
        self.secretary_remarks = str(df['Secretary Remarks'])
        self.agenda_item_sort_order = str(df['Agenda item sort order'])
        self.agenda_item = str(df['Agenda item'])
        self.agenda_item_description = str(df['Agenda item description'])
        self.tdoc_sort_order_within_agenda_item = str(df['TDoc sort order within agenda item'])
        self.tdoc_status = str(df['TDoc Status'])
        self.reservation_date = str(df['Reservation date'])
        self.uploaded = str(df['Uploaded'])
        self.is_revision_of = str(df['Is revision of'])
        self.revised_to = str(df['Revised to'])
        self.release = str(df['Release'])
        self.spec = str(df['Spec'])
        self.version = str(df['Version'])
        self.related_wis = str(df['Related WIs'])
        self.cr = str(df['CR'])
        self.cr_revision = str(df['CR revision'])
        self.cr_category = str(df['CR category'])
        self.tsg_cr_pack = str(df['TSG CR Pack'])
        self.reply_to = str(df['Reply to'])
        self.to = str(df['To'])
        self.cc = str(df['Cc'])
        self.original_ls = str(df['Original LS'])
        self.reply_in = str(df['Reply in'])

        self.meeting = self.meeting_


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)