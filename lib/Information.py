from telethon import TelegramClient, events
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re  # ✅ needed for parsing Proxy.txt

# =========================
# Step 1 — Load proxies
# =========================
def load_proxies_from_file(filename="Proxy.txt"):
    proxies = []
    pattern = r'https://t\.me/proxy\?server=(.+)&port=(\d+)&secret=([\w\d]+)'

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = re.match(pattern, line)
            if match:
                server, port, secret = match.groups()
                proxies.append({
                    "addr": server,
                    "port": int(port),
                    "secret": secret
                })
    return proxies

# =========================
# Step 2 — Basic config
# =========================
admin_user_id = 8357183504
api_id = 28235170
api_hash = '07dc5ca51b7f35cac682af9d3912792b'
helper_username = 'Self_Helper_Ultra_Bot'
bot_token = '8514943429:AAEqWGUpIUAc3-uABsEzzdzDm98NSS0wuus'

client_id = '01e7dc6b41c3471b94efe87abeb05919'
client_secret = '4f5f93af1ced4b0d9ba8440606803639'

# =========================
# Step 3 — Load proxies & create client
# =========================
MT_PROTO_PROXIES = load_proxies_from_file("Proxy.txt")

from telethon import TelegramClient, connection
import base64

def base64_secret_to_hex(secret_b64: str) -> str:
    secret_bytes = base64.b64decode(secret_b64 + '=' * (-len(secret_b64) % 4))
    return secret_bytes.hex()

def create_client_with_proxies(api_id, api_hash, proxies):
    for i, p in enumerate(proxies, 1):
        try:
            secret_hex = base64_secret_to_hex(p['secret'])
            print(f"🌐 Trying MTProto proxy {i}/{len(proxies)} → {p['addr']}:{p['port']} secret={secret_hex}")
            
            client = TelegramClient(
                'TRself-MT',
                api_id,
                api_hash,
                connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
                proxy=(p['addr'], p['port'], secret_hex),
                receive_updates=True
            )
            return client
        except Exception as e:
            print(f"❌ Proxy failed: {e}")
    raise RuntimeError("No MTProto proxies worked")


client = create_client_with_proxies(api_id, api_hash, MT_PROTO_PROXIES)
print("CLIENT CREATED:", id(client))

# =========================
# Step 4 — Spotify setup
# =========================
spotify_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=spotify_credentials)

# =========================
# Step 5 — Optional debug handler
# =========================
@client.on(events.NewMessage(outgoing=True))
async def __debug_outgoing(event):
    print("OUTGOING UPDATE:", event.raw_text)
