import os
import openai, groq, docx
from win32com import client as wc
from sae_3gpp_web.settings import GROQ_API_KEY
import pythoncom


def read_docx(path):
    """Lit le contenu d'un fichier doc docx."""
    pythoncom.CoInitialize() 
    w = wc.Dispatch('Word.Application')
    doc=w.Documents.Open(os.path.abspath(path))
    text = doc.Content.Text
    doc.Close()
    w.Quit()
    return text

def ai_call(text, request_msg):
    client = groq.Groq(
        api_key=GROQ_API_KEY,
    )
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "Tu es un assistant qui traites les documents texte"},
            {"role": "user", "content": f"{request_msg} : {text}"}
        ],
        max_tokens=200
    )
    return response.dict()["choices"][0]["message"]["content"]

def generate_problem(text):
    return ai_call(text, 'c\'est quoi la problématique dans ce texte, si tu ne trouves rien réponds par N/A')


def generate_solution(text):
    return ai_call(text, 'c\'est quoi la solution dans ce texte, si tu ne trouves rien réponds par N/A')


def generate_topic(text):
    return ai_call(text, 'c\'est quoi le topic de ce texte')

def generate_summary(text):
    return ai_call(text, 'Résume ce texte')

def generate_content(text):
    return ai_call(text, 'Donne moi le contenu pretinent de ce texte')

def get_ai_fields(doc_path):
    text = read_docx(doc_path)
    content = generate_content(text[:5000])
    return {
        "content":content,
        "topic":generate_topic(content),
        "summary":generate_summary(content),
        "problem":generate_problem(content),
        "solution":generate_solution(content),
    }


# if __name__ == "__main__":
#     # Charger le document
#     text = read_docx()

#     # Générer le résumé
#     topic = generate_topic(text)
#     problem = generate_problem(text)
#     solution = generate_solution(text)

#     # Afficher le résumé
#     with open("ai.txt", "w") as f:
#         f.writelines([
#             "\nContenu du fichier:",
#             f"\n{text}",
#             "\nRéponse de l'IA sur le fichier : "
#             f"\ntopic: {topic}",
#             f"\nproblem: {problem}",
#             f"\nsolution: {solution}"
#         ])
