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

    
def register_vote(vote_data,user_id: str, vereador_number: str, prefeito_number: str):
    presence_data = {
        "user_id": user_id,
        "timestamp": datetime.datetime.now().isoformat()  
    }
    data_to_sign = (presence_data['user_id'] + presence_data['timestamp']).encode()
    presence_data["signature"] = sign_data(f"./crypto/keys/{user_id}", data_to_sign).hex()

    vote_vereador, v_user_pin, v_tse_pin = generate_vote_obj(user_id, "vereador", vereador_number)
    vote_prefeito, p_user_pin, p_user_pin = generate_vote_obj(user_id, "prefeito", prefeito_number)

    vote_data["presences"].append(presence_data)
    vote_data["votes"].append(vote_vereador)
    vote_data["votes"].append(vote_prefeito)

    return {
        "presence_data": presence_data,
        "vote_vereador": vote_vereador,
        "vote_prefeito": vote_prefeito,
        "user_pin_vereador": v_user_pin,
        "tse_pin_vereador": v_tse_pin,
        "user_pin_prefeito": p_user_pin,
        "tse_pin_prefeito": p_user_pin,
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

    vote["hash"] = generate_hash(user_id + user_pin + tse_pin)

    return vote, user_pin, tse_pin

def generate_random_hash():
    random_data = os.urandom(32)  
    hash_object = hashlib.sha256(random_data)
    random_hash = hash_object.hexdigest()
    return random_hash[:20]

def end_voting(vote_data): 
    vote_data["presences"].sort(key=lambda x: x["timestamp"])
    vote_data["votes"].sort(key=lambda x: x["hash"])
    data_to_sign = json.dumps(vote_data).replace(" ", "")
    vote_data["signature"] = sign_data(f"./crypto/keys/ballot", data_to_sign.encode()).hex()
    with open(f"./session_data/{vote_data['session']}_{vote_data['zone']}.sess", "w") as json_file:
        json.dump(vote_data, json_file, indent=4)


def simulate_session(city, state, session, zone):
    print(f"simulating {city} {state} {session} {zone}")
    vote_data = {
        "presences": [],
        "votes": [],
        "city": city.replace(" ", "_"),
        "state": state, 
        "session": session,
        "zone": zone.replace(" ", "_")
    }
    city_candidates = candidates[city]
    
    for voter in voters:
        vereador = str(city_candidates["vereador"][random.randint(0, 1)])
        prefeito = str(city_candidates["prefeito"][random.randint(0, 1)])
        register_vote(vote_data, voter, vereador, prefeito)

    end_voting(vote_data)

def simulate_voting():
    simulate_session("Curitiba", "PR", "077", "UTFPR")
    simulate_session("São Paulo", "SP", "078", "USP")
    simulate_session("Votuporanga", "SP", "001", "Faculdade Futura")
    simulate_session("Curitiba", "PR", "005", "UFPR")
    simulate_session("Rio de Janeiro", "RJ", "101", "UFRJ")
    simulate_session("Florianópolis", "SC", "023", "UFSC")
    simulate_session("Porto Alegre", "RS", "045", "UFRGS")
    simulate_session("Belo Horizonte", "MG", "056", "UFMG")
    simulate_session("Campinas", "SP", "090", "UNICAMP")
    simulate_session("Salvador", "BA", "067", "UFBA")
    simulate_session("Fortaleza", "CE", "112", "UFC")
    simulate_session("Curitiba", "PR", "014", "PUCPR")
    simulate_session("Londrina", "PR", "033", "UEL")
    simulate_session("Foz do Iguaçu", "PR", "088", "UNILA")
    simulate_session("São Carlos", "SP", "043", "UFSCar")
    simulate_session("Vitória", "ES", "065", "UFES")
    simulate_session("João Pessoa", "PB", "086", "UFPB")
    simulate_session("Natal", "RN", "087", "UFRN")
    simulate_session("Belém", "PA", "076", "UFPA")
    simulate_session("Manaus", "AM", "092", "UFAM")
    simulate_session("Brasília", "DF", "121", "UnB")
    simulate_session("Aracaju", "SE", "031", "UFS")
    simulate_session("Recife", "PE", "060", "UFPE")
    simulate_session("Maceió", "AL", "053", "UFAL")
    simulate_session("Teresina", "PI", "042", "UFPI")
    simulate_session("Campo Grande", "MS", "039", "UFMS")
    simulate_session("Cuiabá", "MT", "032", "UFMT")
    simulate_session("Goiânia", "GO", "057", "UFG")
    simulate_session("Palmas", "TO", "058", "UFT")
    simulate_session("São Luís", "MA", "064", "UFMA")
    simulate_session("Macapá", "AP", "020", "UNIFAP")
    simulate_session("Boa Vista", "RR", "019", "UFRR")
    simulate_session("Rio Branco", "AC", "009", "UFAC")
    simulate_session("Porto Velho", "RO", "022", "UNIR")
    simulate_session("São Paulo", "SP", "054", "Mackenzie")
    simulate_session("Curitiba", "PR", "013", "Unicuritiba")
    simulate_session("Florianópolis", "SC", "034", "UNISUL")
    simulate_session("Porto Alegre", "RS", "027", "PUCRS")
    simulate_session("Belo Horizonte", "MG", "038", "PUCMG")
    simulate_session("Campinas", "SP", "099", "PUC Campinas")
    simulate_session("Salvador", "BA", "085", "UNIFACS")
    simulate_session("Fortaleza", "CE", "105", "UNIFOR")
    simulate_session("Curitiba", "PR", "011", "UTFPR")
    simulate_session("Londrina", "PR", "030", "Unopar")
    simulate_session("Foz do Iguaçu", "PR", "091", "UNILA")
    simulate_session("São Carlos", "SP", "050", "USP São Carlos")
    simulate_session("Vitória", "ES", "070", "FAESA")
    simulate_session("João Pessoa", "PB", "080", "IESP")
    simulate_session("Natal", "RN", "083", "UNP")
    simulate_session("Belém", "PA", "068", "CESUPA")

    


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
  "Aracaju": {
    "prefeito": [
      961993,
      599906
    ],
    "vereador": [
      514,
      790
    ]
  },
  "Belém": {
    "prefeito": [
      592895,
      295429
    ],
    "vereador": [
      786,
      792
    ]
  },
  "Belo Horizonte": {
    "prefeito": [
      701600,
      559964
    ],
    "vereador": [
      106,
      293
    ]
  },
  "Boa Vista": {
    "prefeito": [
      193106,
      720445
    ],
    "vereador": [
      897,
      708
    ]
  },
  "Brasília": {
    "prefeito": [
      365860,
      680051
    ],
    "vereador": [
      768,
      256
    ]
  },
  "Campinas": {
    "prefeito": [
      480985,
      812107
    ],
    "vereador": [
      870,
      262
    ]
  },
  "Campo Grande": {
    "prefeito": [
      255213,
      799459
    ],
    "vereador": [
      928,
      572
    ]
  },
  "Cuiabá": {
    "prefeito": [
      471307,
      123361
    ],
    "vereador": [
      158,
      344
    ]
  },
  "Curitiba": {
    "prefeito": [
      201346,
      898999
    ],
    "vereador": [
      537,
      457
    ]
  },
  "Florianópolis": {
    "prefeito": [
      873519,
      329163
    ],
    "vereador": [
      530,
      863
    ]
  },
  "Fortaleza": {
    "prefeito": [
      162390,
      953989
    ],
    "vereador": [
      484,
      472
    ]
  },
  "Foz do Iguaçu": {
    "prefeito": [
      625147,
      230747
    ],
    "vereador": [
      358,
      404
    ]
  },
  "Goiânia": {
    "prefeito": [
      974365,
      287176
    ],
    "vereador": [
      736,
      670
    ]
  },
  "João Pessoa": {
    "prefeito": [
      750777,
      646142
    ],
    "vereador": [
      889,
      168
    ]
  },
  "Londrina": {
    "prefeito": [
      461698,
      483504
    ],
    "vereador": [
      250,
      640
    ]
  },
  "Macapá": {
    "prefeito": [
      946879,
      718694
    ],
    "vereador": [
      334,
      584
    ]
  },
  "Maceió": {
    "prefeito": [
      896319,
      955168
    ],
    "vereador": [
      354,
      496
    ]
  },
  "Manaus": {
    "prefeito": [
      706316,
      115189
    ],
    "vereador": [
      929,
      490
    ]
  },
  "Natal": {
    "prefeito": [
      962805,
      341694
    ],
    "vereador": [
      779,
      432
    ]
  },
  "Palmas": {
    "prefeito": [
      928139,
      708183
    ],
    "vereador": [
      990,
      817
    ]
  },
  "Porto Alegre": {
    "prefeito": [
      448819,
      610495
    ],
    "vereador": [
      500,
      796
    ]
  },
  "Porto Velho": {
    "prefeito": [
      221060,
      950434
    ],
    "vereador": [
      584,
      453
    ]
  },
  "Recife": {
    "prefeito": [
      419359,
      456149
    ],
    "vereador": [
      627,
      665
    ]
  },
  "Rio Branco": {
    "prefeito": [
      887992,
      908956
    ],
    "vereador": [
      949,
      586
    ]
  },
  "Rio de Janeiro": {
    "prefeito": [
      127101,
      853900
    ],
    "vereador": [
      371,
      960
    ]
  },
  "Salvador": {
    "prefeito": [
      483004,
      275305
    ],
    "vereador": [
      285,
      394
    ]
  },
  "São Carlos": {
    "prefeito": [
      680112,
      443292
    ],
    "vereador": [
      437,
      441
    ]
  },
  "São Luís": {
    "prefeito": [
      409765,
      767606
    ],
    "vereador": [
      828,
      500
    ]
  },
  "São Paulo": {
    "prefeito": [
      788307,
      320464
    ],
    "vereador": [
      505,
      856
    ]
  },
  "Teresina": {
    "prefeito": [
      271342,
      629451
    ],
    "vereador": [
      499,
      941
    ]
  },
  "Vitória": {
    "prefeito": [
      444217,
      952364
    ],
    "vereador": [
      363,
      152
    ]
  },
  "Votuporanga": {
    "prefeito": [
      121447,
      759948
    ],
    "vereador": [
      427,
      792
    ]
  }
} 

if __name__ == "__main__":
    simulate_voting()
