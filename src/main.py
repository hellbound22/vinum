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

@server.route("/cadastro_expositor", methods=["POST"])
def cadastro_expositor():
    expositor = json.loads(request.data.decode("UTF-8"))

    if ("expositor" not in expositor) or ("cpf" not in expositor) or ("cidade" not in expositor) or ("email" not in expositor) or ("hash" not in expositor):
        return {"erro": "Cadastro Incompleto"}, status.HTTP_406_NOT_ACCEPTABLE
    
    else:
        cadastrado = db_expositores.find_one({"cpf": expositor["cpf"]})
        if cadastrado is not None:
            return {"erro": "Exposutor já cadastrado"}, status.HTTP_409_CONFLICT
        else:
            db_expositores.insert_one(expositor)

            return {}, status.HTTP_201_CREATED
    
    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

@server.route("/cadastro_visitante", methods=["POST"])
def cadastro_visitante():
    import interno 
    visitante = json.loads(request.data.decode("UTF-8"))

    if ("nome" not in visitante) or ("cpf" not in visitante) or ("nascimento" not in visitante) or ("cidade" not in visitante):
        return {"erro": "Cadastro Incompleto"}, status.HTTP_406_NOT_ACCEPTABLE
    
    else:
        cadastrado = db_visitantes.find_one({"cpf": visitante["cpf"]})
        if cadastrado is not None:
            return {"erro": "Usuário já cadastrado"}, status.HTTP_409_CONFLICT
        else:
            nova_comanda = interno.criar_comanda(visitante["nome"])
            comanda = db_comandas.insert_one(nova_comanda).inserted_id
            
            visitante["comandas"] = [ comanda ]

            db_visitantes.insert_one(visitante)

            return {"nmr_comanda": nova_comanda["nmr"]}, status.HTTP_201_CREATED

    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

def start_server():
    server.run(use_reloader=False)


if __name__ == "__main__":
    start_server()
