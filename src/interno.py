from main import db_comandas

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


