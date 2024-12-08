from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import  padding
import random
import datetime
import json
import hashlib
import os



def sign_data(private_key_path: str, data: str) -> str:
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

    
def register_vote(vote_data, tse_data, user_data, user_id: str, vereador_number: str, prefeito_number: str):
    presence_data = {
        "user_id": user_id,
        "timestamp": str(datetime.datetime.now().timestamp()).split(".")[0]  
    }
    data_to_sign = (presence_data['user_id'] + presence_data['timestamp']).encode()
    presence_data["signature"] = sign_data(f"./crypto/keys/{user_id}", data_to_sign).hex()

    vote_vereador, v_user_pin, v_tse_pin = generate_vote_obj(user_id, "vereador", vereador_number)
    vote_prefeito, p_user_pin, p_tse_pin = generate_vote_obj(user_id, "prefeito", prefeito_number)

    vote_data["presences"].append(presence_data)
    vote_data["votes"].append(vote_vereador)
    vote_data["votes"].append(vote_prefeito)

    tse_data.append({"user_id": user_id, "position": "vereador", "pin": v_tse_pin})
    tse_data.append({"user_id": user_id, "position": "prefeito", "pin": p_tse_pin})

    user_data.append({"user_id": user_id, "position": "vereador", "pin": v_user_pin})
    tse_data.append({"user_id": user_id, "position": "prefeito", "pin": p_user_pin})

    return {
        "user_id": user_id,
        "presence_data": presence_data,
        "vote_vereador": vote_vereador,
        "vote_prefeito": vote_prefeito,
        "user_pin_vereador": v_user_pin,
        "tse_pin_vereador": v_tse_pin,
        "user_pin_prefeito": p_user_pin,
        "tse_pin_prefeito": p_tse_pin,
    }

def generate_hash(data: str):
    hash_object = hashlib.sha256(data.encode())
    random_hash = hash_object.hexdigest()
    return random_hash

def generate_vote_obj(user_id: str, position: str, candidate_number: str):
    vote = {
      "position": position,
      "candidate": candidate_number,
    }

    user_pin = generate_random_hash()
    tse_pin = generate_random_hash()
    print(user_id, user_pin, tse_pin)
    vote["hash"] = generate_hash(user_id + user_pin + tse_pin)
    print(vote["hash"])
    return vote, user_pin, tse_pin

def generate_random_hash():
    random_data = os.urandom(32)  
    hash_object = hashlib.sha256(random_data)
    random_hash = hash_object.hexdigest()
    return random_hash[:20]

def end_voting(vote_data, tse_data,user_data): 
    vote_data["presences"].sort(key=lambda x: x["timestamp"])
    vote_data["votes"].sort(key=lambda x: x["hash"])
    data_to_sign = json.dumps(vote_data).replace(" ", "")
    vote_data["signature"] = sign_data(f"./crypto/keys/ballot", data_to_sign.encode()).hex()
    session_path = f"./session_data/{vote_data['section']}_{vote_data['zone']}"
    with open(f"{session_path}.sess", "w") as json_file:
        json.dump(vote_data, json_file, indent=4)
    with open(f"{session_path}.tse", "w") as json_file:
        json.dump(tse_data, json_file, indent=4)
    with open(f"{session_path}.user", "w") as json_file:
        json.dump(user_data, json_file, indent=4)


def simulate_session(city, state, session, zone):
    print(f"simulating {city} {state} {session} {zone}")
    vote_data = {
        "presences": [],
        "votes": [],
        "city": city.replace(" ", "_"),
        "state": state, 
        "section": session,
        "zone": zone.replace(" ", "_")
    }
    tse_data = []
    user_data = []
    city_candidates = candidates[city]
    
    for voter in voters:
        vereador = str(city_candidates["vereador"][random.randint(0, 1)])
        prefeito = str(city_candidates["prefeito"][random.randint(0, 1)])
        register_vote(vote_data, tse_data, user_data, voter, vereador, prefeito)

    end_voting(vote_data, tse_data, user_data)

def simulate_voting():
    simulate_session("Curitiba", "PR", "077", "UTFPR")
    simulate_session("Sao Paulo", "SP", "078", "USP")
    simulate_session("Votuporanga", "SP", "001", "Faculdade Futura")
    simulate_session("Curitiba", "PR", "005", "UFPR")
    simulate_session("Rio de Janeiro", "RJ", "101", "UFRJ")
    simulate_session("Florianopolis", "SC", "023", "UFSC")
    simulate_session("Porto Alegre", "RS", "045", "UFRGS")
    simulate_session("Belo Horizonte", "MG", "056", "UFMG")
    simulate_session("Campinas", "SP", "090", "UNICAMP")
    simulate_session("Salvador", "BA", "067", "UFBA")
    simulate_session("Fortaleza", "CE", "112", "UFC")
    simulate_session("Curitiba", "PR", "014", "PUCPR")
    simulate_session("Londrina", "PR", "033", "UEL")
    simulate_session("Foz do Iguacu", "PR", "088", "UNILA")
    simulate_session("Sao Carlos", "SP", "043", "UFSCar")
    simulate_session("Vitoria", "ES", "065", "UFES")
    simulate_session("Joao Pessoa", "PB", "086", "UFPB")
    simulate_session("Natal", "RN", "087", "UFRN")
    simulate_session("Belem", "PA", "076", "UFPA")
    simulate_session("Manaus", "AM", "092", "UFAM")
    simulate_session("Brasilia", "DF", "121", "UnB")
    simulate_session("Aracaju", "SE", "031", "UFS")
    simulate_session("Recife", "PE", "060", "UFPE")
    simulate_session("Maceio", "AL", "053", "UFAL")
    simulate_session("Teresina", "PI", "042", "UFPI")
    simulate_session("Campo Grande", "MS", "039", "UFMS")
    simulate_session("Cuiaba", "MT", "032", "UFMT")
    simulate_session("Goiânia", "GO", "057", "UFG")
    simulate_session("Palmas", "TO", "058", "UFT")
    simulate_session("Sao Luis", "MA", "064", "UFMA")
    simulate_session("Macapa", "AP", "020", "UNIFAP")
    simulate_session("Boa Vista", "RR", "019", "UFRR")
    simulate_session("Rio Branco", "AC", "009", "UFAC")
    simulate_session("Porto Velho", "RO", "022", "UNIR")
    simulate_session("Sao Paulo", "SP", "054", "Mackenzie")
    simulate_session("Curitiba", "PR", "013", "Unicuritiba")
    simulate_session("Florianopolis", "SC", "034", "UNISUL")
    simulate_session("Porto Alegre", "RS", "027", "PUCRS")
    simulate_session("Belo Horizonte", "MG", "038", "PUCMG")
    simulate_session("Campinas", "SP", "099", "PUC Campinas")
    simulate_session("Salvador", "BA", "085", "UNIFACS")
    simulate_session("Fortaleza", "CE", "105", "UNIFOR")
    simulate_session("Curitiba", "PR", "011", "UTFPR")
    simulate_session("Londrina", "PR", "030", "Unopar")
    simulate_session("Foz do Iguacu", "PR", "091", "UNILA")
    simulate_session("Sao Carlos", "SP", "050", "USP Sao Carlos")
    simulate_session("Vitoria", "ES", "070", "FAESA")
    simulate_session("Joao Pessoa", "PB", "080", "IESP")
    simulate_session("Natal", "RN", "083", "UNP")
    simulate_session("Belem", "PA", "068", "CESUPA")

    


voters = [
    "5b5a6ffb5ddb48097f1f",
    "ce805f56ff64ce9f1bf8",
    "56f326b0e23fb765963f",
    "5887c27b14664077e318",
    "b46338b9eb513bfaafc5",
    "8788f46a439f4f718757",
    "d7b977712bc0aa6acdf1",
    "c6f07accdb016a24396e",
    "10b82744669347897ab5",
    "a5ec5c49eef382efcc1e",
    "50a4be92c301dc113063",
    "708e6f27e52e476cfe1d",
    "090adfab610ac04c63ab",
    "01b8b186a1d869910136",
    "781ae0d88daa1bbd7b4a",
    "14f4e0a1a724842873e2",
    "71df18ad8337037d720a",
    "9f2e4b1356c648e1a2aa",
    "f6b518b2ecd9f47761ed",
    "fd7de658119bf6541d49"
]

candidates = {
  "Aracaju": { "prefeito": [96199, 59990], "vereador": [51, 79] },
  "Belem": { "prefeito": [59289, 29542], "vereador": [78, 79] },
  "Belo Horizonte": { "prefeito": [70160, 55996], "vereador": [10, 29] },
  "Boa Vista": { "prefeito": [19310, 72044], "vereador": [89, 70] },
  "Brasilia": { "prefeito": [36586, 68005], "vereador": [76, 25] },
  "Campinas": { "prefeito": [48098, 81210], "vereador": [87, 26] },
  "Campo Grande": { "prefeito": [25521, 79945], "vereador": [92, 57] },
  "Cuiaba": { "prefeito": [47130, 12336], "vereador": [15, 34] },
  "Curitiba": { "prefeito": [20134, 89899], "vereador": [53, 45] },
  "Florianopolis": { "prefeito": [87351, 32916], "vereador": [53, 86] },
  "Fortaleza": { "prefeito": [16239, 95398], "vereador": [48, 47] },
  "Foz do Iguacu": { "prefeito": [62514, 23074], "vereador": [35, 40] },
  "Goiânia": { "prefeito": [97436, 28717], "vereador": [73, 67] },
  "Joao Pessoa": { "prefeito": [75077, 64614], "vereador": [88, 16] },
  "Londrina": { "prefeito": [46169, 48350], "vereador": [25, 64] },
  "Macapa": { "prefeito": [94687, 71869], "vereador": [33, 58] },
  "Maceio": { "prefeito": [89631, 95516], "vereador": [35, 49] },
  "Manaus": { "prefeito": [70631, 11518], "vereador": [92, 49] },
  "Natal": { "prefeito": [96280, 34169], "vereador": [77, 43] },
  "Palmas": { "prefeito": [92813, 70818], "vereador": [99, 81] },
  "Porto Alegre": { "prefeito": [44881, 61049], "vereador": [50, 79] },
  "Porto Velho": { "prefeito": [22106, 95043], "vereador": [58, 45] },
  "Recife": { "prefeito": [41935, 45614], "vereador": [62, 66] },
  "Rio Branco": { "prefeito": [88799, 90895], "vereador": [94, 58] },
  "Rio de Janeiro": { "prefeito": [12710, 85390], "vereador": [37, 96] },
  "Salvador": { "prefeito": [48300, 27530], "vereador": [28, 39] },
  "Sao Carlos": { "prefeito": [68011, 44329], "vereador": [43, 44] },
  "Sao Luis": { "prefeito": [40976, 76760], "vereador": [82, 50] },
  "Sao Paulo": { "prefeito": [78830, 32046], "vereador": [50, 85] },
  "Teresina": { "prefeito": [27134, 62945], "vereador": [49, 94] },
  "Vitoria": { "prefeito": [44421, 95236], "vereador": [36, 15] },
  "Votuporanga": { "prefeito": [12144, 75994], "vereador": [42, 79] }
}


if __name__ == "__main__":
    simulate_voting()
