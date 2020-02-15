from main import db_comandas, db_visitantes

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

def adicionar_comanda_a_visitante(cpf):
    comanda = criar_comanda(cpf)
    id_comanda = db_comandas.insert_one(comanda).inserted_id

    lista_anterior = db_visitantes.find_one({"cpf": cpf})

    lista = dict(lista_anterior)["comandas"]
    if lista is None:
        lista = [id_comanda]
    else: 
        lista.append(id_comanda)

    db_visitantes.find_one_and_update({"cpf": cpf}, {"$set": 
        {"comandas": lista}})

def lista_comandas_cpf(cpf):
    visitante = db_visitantes.find_one({"cpf": cpf})

    if visitante is None:
        return visitante

    return dict(visitante)["comandas"]

def apagar_comanda_nmr(nmr):
    return db_comandas.find_one_and_delete({"nmr": nmr})

def apagar_visitante(cpf):
    return db_visitantes.find_one_and_delete({"cpf": cpf})



