import json
import pymongo

from flask import Flask
from flask import request, abort
from flask_api import status

MONGO_SERVER = "ec2-18-222-148-185.us-east-2.compute.amazonaws.com" 

client = pymongo.MongoClient(MONGO_SERVER)

db_visitantes = client["vinum"]["visitantes"]
db_comandas = client["vinum"]["comandas"]
db_expositores = client["vinum"]["expositores"]
db_controle = client["vinum"]["controle"]

server = Flask(__name__)

@server.route("/cadastro_visitante", methods=["POST"])
def cadastro_visitante():
    visitante = json.loads(request.data.decode("UTF-8"))

    cadastrado = db_visitantes.find_one({"cpf": visitante["cpf"]})
    if cadastrado is not None:
        return {"erro": "Usuário já cadastrado"}, status.HTTP_409_CONFLICT
    else:
        nova_comanda = criar_comanda(visitante["nome"])
        comanda = db_comandas.insert_one(nova_comanda).inserted_id
        
        visitante["comandas"] = [ comanda ]

        db_visitantes.insert_one(visitante)

        return {"nmr_comanda": nova_comanda["nmr"]}, status.HTTP_201_CREATED

    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

def criar_comanda(visi):
    ultimo_nmr = db_comandas.find()

    try:
        ultimo_nmr = dict(list(ultimo_nmr)[::-1][0])["nmr"]
    except:
        ultimo_nmr = 0

    return {
            "nmr": int(ultimo_nmr) + 1, # Provavelmente dá pra retirar essa cast
            "dono": visi,
            "vales": 2,
            "visitas": []
            }

def start_server():
    server.run(use_reloader=False)

start_server()
