from flask import Blueprint, request, jsonify, render_template
from app import dsa, qa
from dotenv import load_dotenv
import os
from transformers import AutoModelWithLMHead, AutoTokenizer

load_dotenv()

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
saved_model = AutoModelWithLMHead.from_pretrained("pragadeshbs/dialoGPT-finetune")

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

bp = Blueprint("app", __name__)


# def answer_based_on_context(question):
#     payload = {
#         "inputs": {
#             "question": question,
#             "context": "A crowded railway station is a hub of activity, a microcosm of life itself. The station is bustling with people from all walks of life, each with their own story to tell. The air is filled with the cacophony of sounds - the chatter of passengers, the loudspeaker announcements, the clatter of luggage, and the occasional whistle of a train pulling into or out of the station. The ticket counter, located inside the station building right next to the platform, is a scene of organized chaos. There's a long queue of passengers waiting patiently to buy their tickets, while the ticketing staff work efficiently, issuing tickets and providing information to the travelers. The platform itself is a hive of activity. Passengers are scattered everywhere - some are waiting for their trains, others are saying their goodbyes, while a few are rushing to catch their train. The vendors are busy selling their wares, adding to the vibrant atmosphere of the station. The trains passing by the station add a dynamic element to the scene. The powerful engines pull in and out of the station, their carriages filled with passengers. Each train arrival and departure is a spectacle in itself, signaling a wave of activity on the platform.",
#         },
#     }
#     response = requests.post(API_URL, headers=headers, json=payload)
#     print(response.json())
#     return response.json()["answer"]


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/api/analyze", methods=["POST", "GET"])
def dsaResult():
    if request.method == "POST":
        text = request.form["text"]
        lst = dsa.ret_results(text)
        print(lst)
        result = {
            "depression": str(lst[0]) + "/10",
            "anxiety": str(lst[1]) + "/10",
            "stress": str(lst[2]) + "/10",
        }
        return jsonify(result)


@bp.route("/api/answer", methods=["POST"])
def getAnswer():
    if request.method == "POST":
        text = request.form["question"]
        answer = qa.get_reponse_for_question(text, tokenizer, saved_model)
        result = {"answer": answer}
        return jsonify(result)
