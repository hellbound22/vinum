import json
import pymongo
import jwt
import datetime

from flask import Flask, jsonify
from flask import request, abort
from flask_api import status

from werkzeug.security import safe_str_cmp

MONGO_SERVER = "127.0.0.1" 
PRECO_FICHA = 5
FICHAS_GRATIS = 3

client = pymongo.MongoClient(MONGO_SERVER, connect=False)

DB_VISITANTES = client["vinum"]["visitantes"]
DB_COMANDAS = client["vinum"]["comandas"]
DB_EXPOSITORES = client["vinum"]["expositores"]
DB_CONTROLE = client["vinum"]["controle"]
DB_AUTH = client["vinum"]["auth"]

server = Flask(__name__)
server.config['SECRET_KEY'] = 'testevinum'

@server.route("/gen_auth", methods=["POST"])
def gen_auth():
    import src.interno
    data = json.loads(request.data.decode("UTF-8"))
    
    user = db_auth.find_one({"user": data["user"]})
    
    if user is not None and safe_str_cmp(user["hash"], data["hash"]):
        token = jwt.encode({"user": user["user"], "role": user["role"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, server.config["SECRET_KEY"])

        return {"token": token.decode("UTF-8"), "role": user["role"], "cpf": user["cpf"]}, status.HTTP_201_CREATED


@server.route("/controle/trancar", methods=["POST"])
def trancar_comanda(): 
    import src.interno
    if "Jwt-Token" not in request.headers:
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    token = request.headers["Jwt-Token"]
    auth = src.interno.check_auth(token)

    if auth is not False and not safe_str_cmp(auth["role"].encode("UTF-8"), "adm".encode("UTF-8")):
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    data = json.loads(request.data.decode("UTF-8"))

    if ("comanda" not in data) or ("cpf_associado" not in data):
        return {"erro": "Dados Incompletos"}, status.HTTP_406_NOT_ACCEPTABLE

    comanda = db_comandas.find_one({"nmr": data["comanda"]})
    
    if comanda is None:
        return {"erro": "Impossível achar comanda"}, status.HTTP_404_NOT_FOUND

    elif comanda["dono"] != data["cpf_associado"]:
        return {"erro": "CPF não corresponde ao dono da comanda"}, status.HTTP_406_NOT_ACCEPTABLE

    else:
        confirm = src.interno.travar_comanda_id(comanda["_id"])
        if confirm is not None:
            return {}, status.HTTP_200_OK

    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

def check_role(auth, role):
    return auth is not False and not safe_str_cmp(auth["role"].encode("UTF-8"), role.encode("UTF-8"))

@server.route("/controle/acerto/<nmr>", methods=["GET"])
def get_comanda_final(nmr): 
    import src.interno
    if "Jwt-Token" not in request.headers:
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    token = request.headers["Jwt-Token"]
    auth = src.interno.check_auth(token)
    
    if check_role(auth, "adm"):
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    comanda = db_comandas.find_one({"nmr": int(nmr)})

    if comanda is None:
        return {"erro": "Impossível achar comanda"}, status.HTTP_404_NOT_FOUND
    else:
        qtd_visitas = 0

        for v in comanda["visitas"]:
            qtd_visitas += int(v["qnt"])
        

        preco_final = PRECO_FICHA * (qtd_visitas - FICHAS_GRATIS)
        
        if preco_final <= 0:
            preco_final = 0

        return {
                "dono": comanda["dono"],
                "nmr_tickets": qtd_visitas,
                "preco_final" : preco_final 
                }


    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR


@server.route("/cadastro_expositor", methods=["POST"])
def cadastro_expositor():
    import src.interno
    if "Jwt-Token" not in request.headers:
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    token = request.headers["Jwt-Token"]
    auth = src.interno.check_auth(token)

    if auth is not False and not safe_str_cmp(auth["role"].encode("UTF-8"), "adm".encode("UTF-8")):
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    expositor = json.loads(request.data.decode("UTF-8"))

    if ("expositor" not in expositor) or ("cpf" not in expositor) or ("cidade" not in expositor) or ("email" not in expositor) or ("hash" not in expositor):
        return {"erro": "Cadastro Incompleto"}, status.HTTP_406_NOT_ACCEPTABLE
    
    else:
        cadastrado = db_expositores.find_one({"cpf": expositor["cpf"]})
        if cadastrado is not None:
            return {"erro": "Expositor já cadastrado"}, status.HTTP_409_CONFLICT
        else:
            expositor["visitas"] = []
            db_expositores.insert_one(expositor)

            auth = {
                    "user": expositor["email"],
                    "cpf": expositor["cpf"],
                    "hash": expositor["hash"],
                    "role" : "exp"
                    }
            db_auth.insert_one(auth)


            return {}, status.HTTP_201_CREATED
    
    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

@server.route("/cadastro_visitante", methods=["POST"])
def cadastro_visitante():
    import src.interno
    if "Jwt-Token" not in request.headers:
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    token = request.headers["Jwt-Token"]
    auth = src.interno.check_auth(token)

    if auth is not False and not safe_str_cmp(auth["role"].encode("UTF-8"), "adm".encode("UTF-8")):
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    visitante = json.loads(request.data.decode("UTF-8"))

    if ("nome" not in visitante) or ("cpf" not in visitante) or ("nascimento" not in visitante) or ("cidade" not in visitante):
        return {"erro": "Cadastro Incompleto"}, status.HTTP_406_NOT_ACCEPTABLE
    
    else:
        cadastrado = db_visitantes.find_one({"cpf": visitante["cpf"]})
        if cadastrado is not None:
            return {"erro": "Usuário já cadastrado"}, status.HTTP_409_CONFLICT
        else:
            nova_comanda = src.interno.criar_comanda(visitante["cpf"])
            comanda = db_comandas.insert_one(nova_comanda).inserted_id
            
            visitante["comandas"] = [ comanda ]

            db_visitantes.insert_one(visitante)

            return {"nmr_comanda": nova_comanda["nmr"]}, status.HTTP_201_CREATED

    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

@server.route("/expositor/cobrar", methods=["POST"])
def cobrar():
    import src.interno
    if "Jwt-Token" not in request.headers:
        return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    token = request.headers["Jwt-Token"]
    auth = src.interno.check_auth(token)

    #if auth is not False:
    #    return {"erro": "Acesso Proibido"}, status.HTTP_401_UNAUTHORIZED

    data = json.loads(request.data.decode("UTF-8"))

    if ("comanda" not in data) or ("qnt" not in data) or ("cpf_expositor" not in data):
        return {"erro": "Informações inconpletas"}, status.HTTP_406_NOT_ACCEPTABLE

    else:
        qtd = data["qnt"]

        # TODO: Verificar se as foi possível achar os dados
        expositor = db_expositores.find_one({"cpf": data["cpf_expositor"]})
        comanda = db_comandas.find_one({"nmr": int(data["comanda"])})
        visitante = db_visitantes.find_one({"cpf": comanda["dono"]})

        if (comanda is None) or (expositor is None) or (visitante is None):
            return {"erro": "Impossível achar alguns atores"}, status.HTTP_404_NOT_FOUND

        #if comanda["travado"] == True:
        #    return {"erro": "Comanda já travada"}, status.HTTP_403_FORBIDDEN

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
        
        return {}, status.HTTP_200_OK 

    return {}, status.HTTP_500_INTERNAL_SERVER_ERROR


def start_server(bind, debug):
    server.run(host=bind, debug=debug)
