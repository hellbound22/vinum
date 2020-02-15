import json
import pymongo

from flask import Flask
from flask import request, abort
from flask_api import status


MONGO_SERVER = "18.222.148.185" 

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
            expositor["visitas"] = []
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
            nova_comanda = interno.criar_comanda(visitante["cpf"])
            comanda = db_comandas.insert_one(nova_comanda).inserted_id
            
            visitante["comandas"] = [ comanda ]

            db_visitantes.insert_one(visitante)

            return {"nmr_comanda": nova_comanda["nmr"]}, status.HTTP_201_CREATED

    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

@server.route("/expositor/cobrar", methods=["POST"])
def cobrar():
    import interno 
    data = json.loads(request.data.decode("UTF-8"))

    qtd = data["qtd"]

    expositor = db_expositores.find_one({"cpf": data["cpf_expositor"]})
    comanda = db_comandas.find_one({"nmr": data["comanda"]})
    visitante = db_visitantes.find_one({"cpf": comanda["dono"]})

    entrada_exp = {
                "visitante": visitante["_id"],
                "qnt": qtd
            }

    entrada_vis = {
                "expositor": expositor["_id"],
                "qnt": qtd
            }
    
    lista_comanda = dict(comanda)["visitas"]
    if lista_comanda is None:
        lista_comanda = [entrada_vis]
    else: 
        lista_comanda.append(entrada_vis)

    lista_expositor = dict(expositor)["visitas"]
    if lista_expositor is None:
        lista_expositor = [entrada_exp]
    else: 
        lista_expositor.append(entrada_exp)

    db_comandas.find_one_and_update({"_id": comanda["_id"]}, {"$set": 
        {"visitas": lista_comanda}})
    db_expositores.find_one_and_update({"_id": expositor["_id"]}, {"$set": 
        {"visitas": lista_expositor}})

    return ""


def start_server():
    import interno

    server.run(use_reloader=False)


if __name__ == "__main__":
    start_server()
