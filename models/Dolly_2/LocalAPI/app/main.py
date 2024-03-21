#¨¨¨¨¨ ¨¨¨¨¨ ¨¨¨¨¨ ¨¨¨¨¨ ¨¨¨¨¨ #
#           Library            #
#_____ _____ _____ _____ _____ #

# General Libraries
import ssl

# FastAPI requierements
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse

# Debug
ssl._create_default_https_context = ssl._create_unverified_context

# LLM
import torch
from instruct_pipeline import InstructionTextGenerationPipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

# ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#      Large Lang. Model        #
# ______________________________#

tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-3b")
model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-3b")

generate_text = InstructionTextGenerationPipeline(model=model, tokenizer=tokenizer)

def generate_text_from(input):
    res = generate_text(input)
    return res[0]["generated_text"]

# ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#       FastAPI describe        #
# ______________________________#

app = FastAPI(
    timeout=1800, # temps de calcul max à 30 min (60s x 30)
    title="👾 Dolly 2.0 API",
    summary="Dolly 2.0 API: A question/answer LLM.",
    description="""
                ## Dolly 2.0 API: A question/answer LLM.
                * This API uses a Large Language Model to answer questions easily.
                """,
    version="0.0.1",
    contact={
        "name": "Gauthier Rammault",
        "url": "https://www.linkedin.com/in/gauthier-rammault/",
    },
    terms_of_service="https://devlaunchers.org/page/terms-and-conditions",
    openapi_tags= [
        {
            "name": "Home",
            "description": "👾 Dolly 2.0 API homepage."
        },
        {
            "name": "Question",
            "description": "👾 Dolly 2.0 API with POST or GET method."
        }
    ]
)

# ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#       FastAPI run app.       #
# ______________________________#

with open("index.html", "r") as html_file:
    # Lire le contenu du fichier HTML dans une variable texte
    html = html_file.read()

@app.get("/", tags=["Home"])
async def get():
    return HTMLResponse(html)

@app.post("/question/", tags=["Question"])
async def question(input_text: str = ""):
    result = generate_text_from(input_text)
    return "Answer: {}".format(result)