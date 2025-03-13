import pandas as pd
from typing import Optional
import concurrent.futures
import requests
import pathlib
import re
import os

from sae_3gpp_web.settings import FTP_SERVER, TDOC_PREFIX, TDOC_PARENT, LINK_REGX, USE_MULTITHREADING,TDOC_LINKS_FILE_NAME
from .models import Documents

def is_file(link:str)->bool:
    return "."  in link.removeprefix(FTP_SERVER)

def get_sub_links(link:str)->list[str]:
    if is_file(link):
        return []
    # Get html content
    content:str = requests.get(link, timeout=3).text
    # Get all links present in html page
    links:list[str] = re.findall(LINK_REGX, content)
    # Get only children links
    return [l for l in links if l.startswith(link) and l!= link]

def get_tdoc_link(links:list[str])->Optional[str]:
    return next(
        (l for l in links if is_file(l) and TDOC_PREFIX in get_file_name(l) and not l.endswith("zip")),
        None
    )

def get_file_name(url:str)->str:
    return url.split("/")[-1] # to have acces to last element -1 

# Global var
tdocs:list[str] = []

def get_all_tdocs(link:str):
    global tdocs
    # Avoid to look into a file but a directory
    if not is_file(link):
        print(f"Looking inside {link}")
        # Recover links of current page
        try:
            if links:=get_sub_links(link):
                # Recover tdoc link
                if tdoc_link:= get_tdoc_link(links):
                    # TDoc found => append it
                    tdocs.append(tdoc_link)
                    print(f"Found TDoc{tdoc_link}")
                # look inside all other links
                if USE_MULTITHREADING:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(executor.map(get_all_tdocs, links))
                else:
                    for l in links:
                        get_all_tdocs(l)
        except Exception:
            pass


def collect():
    global tdocs
    get_all_tdocs(FTP_SERVER)
    with open(TDOC_LINKS_FILE_NAME,"w") as file:
        for l in tdocs:
            file.write(f"{l} \n")

    with open(TDOC_LINKS_FILE_NAME) as f:
        tdocs = [line.strip() for line in f.readlines()] # strip to delet \n 


    for url in tdocs:
        try:
            pd_tdoc: pd.DataFrame=pd.read_excel(url)
            for index, tdoc in pd_tdoc.iterrows(): # to iterate in lines not colomnes 
                doc = Documents(tdoc, url)
                doc.save()
        except Exception as e:
            print(e)

    print("The data base is succesfuly populated !")

