from model import Document, Session
from conf import TDOC_LINKS_FILE_NAME
import pandas as pd



with open(TDOC_LINKS_FILE_NAME) as f :
    urls= [line.strip() for line in f.readlines()]


session = Session()

for i,url in enumerate(urls):
    try:
        pd_tdoc:pd.DataFrame = pd.read_excel(url)
        tdoc_ids = pd_tdoc["TDoc"]
        session.query(Document).filter(Document.tdoc_id.in_(tdoc_ids)).update({
            "url":url
        })
        print(i)
    except Exception as e:
        print(e)
session.commit()
breakpoint()


