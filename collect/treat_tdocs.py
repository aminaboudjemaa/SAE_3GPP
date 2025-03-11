import os
import zipfile

import requests
import io

from ai import get_ai_fields
from model import Document, Session

EXTRACT_TO = "zips/"
session = Session()

def is_docfile(file:str):
    return file.endswith(".docx") or file.endswith(".doc")

tdocs = session.query(Document).filter(
    Document.topic.is_(None),
    Document.url=="https://www.3gpp.org/ftp/tsg_sa/WG2_Arch/TSGS2_116_Vienna/Docs/TDoc_List_Meeting_SA2%23116.xlsm"
).all()
len_tdocs = len(tdocs)
# for each tdoc
for i, tdoc in enumerate(tdocs):
    # get the zip file
    res = requests.get(tdoc.zip_link)
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
            ai_fields = get_ai_fields(file)
            tdoc.topic = ai_fields["topic"]
            tdoc.problem = ai_fields["problem"]
            tdoc.solution = ai_fields["solution"]
            session.add(tdoc)
            session.commit()
            print(f"generated ai fields for {tdoc.tdoc_id}")
            # cleanup zips directory
        for f in files:
            try:
                os.remove(EXTRACT_TO+f)
            except Exception:
                pass
        
    print(f"\rProgress {100*i/len_tdocs:.2f}%", end="", flush=True)

