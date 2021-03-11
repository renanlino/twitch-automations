from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from twitchAPI.pubsub import PubSub
from uuid import UUID
import requests
import time
import json
import sys

##### SETUP #####
EFFECT1_TRIGGER = "IFTTTrigger-1"
EFFECT2_TRIGGER = "IFTTTrigger-2"
EFFECT3_TRIGGER = "IFTTTrigger-3"
AUTH_SCOPES = [AuthScope.BITS_READ, AuthScope.CHANNEL_READ_SUBSCRIPTIONS]

try:
    f = open("secrets.json", "r")
except IOError:
    print("Erro ao abrir o arquivo de segredos: secrets.json")
    sys.exit(1)
try:
    secrets = json.load(f)
except ValueError:
    print("Erro ao ler o arquivo de segredos: formato inválido")
    sys.exit(1)

CHANNEL_NAME = secrets["CHANNEL_NAME"]
EFFECT1_ENDPOINT = "https://mkzense.com/webhook/alexa/{}/{}".format(secrets["IFFT_ALEXA_SKILL_TOKEN"], EFFECT1_TRIGGER)
EFFECT2_ENDPOINT = "https://mkzense.com/webhook/alexa/{}/{}".format(secrets["IFFT_ALEXA_SKILL_TOKEN"], EFFECT2_TRIGGER)
EFFECT3_ENDPOINT = "https://mkzense.com/webhook/alexa/{}/{}".format(secrets["IFFT_ALEXA_SKILL_TOKEN"], EFFECT3_TRIGGER)

def blink_lights(cicles=5, wait=0.5):
    for i in range(cicles):
        requests.get(EFFECT1_ENDPOINT)
        time.sleep(wait)
        requests.get(EFFECT2_ENDPOINT)
        time.sleep(wait)
    requests.get(EFFECT3_ENDPOINT)

def callback_bits(uuid: UUID, data: dict):
    print('[callback_bits] got callback for UUID ' + str(uuid))
    print("[callback_bits] processando mensagem")
    print("\tFrom: {}".format(data["data"]["user_name"]))
    print("\tConteúdo: {}".format(data["data"]["chat_message"]))
    print("\tTimestamp: {}".format(data["data"]["time"]))
    print("\tPiscando luzes...")
    blink_lights(cicles=1, wait=1)
    print("[callback_bits] Ok!")

def callback_subs(uuid: UUID, data: dict):
    print('[callback_subs] got callback for UUID ' + str(uuid))
    print("[callback_subs] processando sub")
    print("\tFrom: {}".format(data["user_name"]))
    print("\tTimestamp: {}".format(data["time"]))
    print("\tPiscando luzes...")
    blink_lights()
    print("[callback_subs] Ok!")

print("Iniciando autenticação do app...")
twitch = Twitch(secrets["TWITCH_APP_ID"], secrets["TWITCH_APP_SECRET"])
twitch.authenticate_app([])

print("Iniciando autenticação do usuário...")
target_scope = AUTH_SCOPES
auth = UserAuthenticator(twitch, target_scope, force_verify=False)

print("\tAutorize o acesso à sua conta da Twitch pelo browser")
token, refresh_token = auth.authenticate()
twitch.set_user_authentication(token, target_scope, refresh_token)

# channel selection
channels_result = twitch.search_channels(query=CHANNEL_NAME, first=1)
channel_id = channels_result['data'][0]['id']
print("\tNome do Canal: {}".format(channels_result['data'][0]['display_name']))
print("\tID do Canal: {}".format(channel_id))

print("Inciando o Twitch PubSub")
pubsub = PubSub(twitch)
pubsub.start()

print("Inciando o listener de bits")
uuid = pubsub.listen_bits(channel_id, callback_bits)

print("Inciando o listener de subs")
uuid = pubsub.listen_channel_subscriptions(channel_id, callback_subs)

print()
input('pressione ENTER para finalizar\n')

print("Encerrando...")
pubsub.unlisten(uuid)
pubsub.stop()
