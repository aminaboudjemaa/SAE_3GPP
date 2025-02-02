from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import pandas as pd

from conf import DB_NAME

# Create an SQLite engine
engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

# Define the base class
Base = declarative_base()

# Define a model class (table)
class Document(Base):
    __tablename__ = 'documents'
    
    tdoc_id = Column(String, primary_key=True)
    url = Column(String)
    title = Column(String)
    source = Column(String)
    contact = Column(String)
    contact_id = Column(String)
    type = Column(String)
    doc_for = Column(String)
    abstract = Column(String)
    secretary_remarks = Column(String)
    agenda_item_sort_order = Column(String)
    agenda_item = Column(String)
    agenda_item_description = Column(String)
    tdoc_sort_order_within_agenda_item = Column(String)
    tdoc_status = Column(String)
    reservation_date = Column(String)
    uploaded = Column(String)
    is_revision_of = Column(String)
    revised_to = Column(String)
    release = Column(String)
    spec = Column(String)
    version = Column(String)
    related_wis = Column(String)
    cr = Column(String)
    cr_revision = Column(String)
    cr_category = Column(String)
    tsg_cr_pack = Column(String)
    reply_to = Column(String)
    to = Column(String)
    cc = Column(String)
    original_ls = Column(String)
    reply_in = Column(String)

    def __repr__(self):
        return f"<Document(tdoc={self.tdoc_id})>"
    
    def __init__(self, df:pd.DataFrame, url:str):
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

# Create the table in the database (if it doesn't already exist)
Base.metadata.create_all(engine)



# Create a session to interact with the database
Session = sessionmaker(bind=engine)
# session = Session()

# Create a new User object
# new_user = Document(name="Alice", age=30)

# Add the user to the session and commit it to the database
# session.add(new_user)
# session.commit()

# Query the users table
# users = session.query(Document).all()
# print(users)

# Close the session
# session.close()
