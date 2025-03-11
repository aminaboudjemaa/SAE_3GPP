import os
import openai, groq, docx
from win32com import client as wc

# Remplacez par votre clé API OpenAI
GROQ_API_KEY = ""

def read_docx(path):
    """Lit le contenu d'un fichier texte."""

    w = wc.Dispatch('Word.Application')
    doc=w.Documents.Open(os.path.abspath("test.docx"))
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
            {"role": "system", "content": "Tu es un assistant qui résume les documents."},
            {"role": "user", "content": f"{request_msg} : {text}"}
        ],
        max_tokens=200
    )
    return response.dict()["choices"][0]["message"]["content"]

def generate_problem(text):
    return ai_call(text, 'c\'est quoi la problématique dans ce texte')


def generate_solution(text):
    return ai_call(text, 'c\'est quoi la solution dans ce texte')


def generate_topic(text):
    return ai_call(text, 'Résume ce texte')

def get_ai_fields(doc_path):
    text = read_docx(doc_path)
    return {
        "topic":generate_topic(text),
        "problem":generate_problem(text),
        "solution":generate_solution(text),
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
