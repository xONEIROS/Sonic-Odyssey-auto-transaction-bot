import json
import os
import time
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
import bip39
from bip32utils import BIP32Key
import base58
import colorama
from colorama import Fore, Style
import requests
import nacl.signing
import logging

colorama.init(autoreset=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
DEVNET_URL = 'https://devnet.sonic.game/'
LAMPORTS_PER_SOL = 1000000000
HEADERS = {'Accept': '*/*','Accept-Encoding': 'gzip, deflate, br, zstd','Accept-Language': 'en-US,en;q=0.9','Cache-Control': 'no-cache','Origin': 'https://odyssey.sonic.game','Pragma': 'no-cache','Priority': 'u=1, i','Referer': 'https://odyssey.sonic.game/','Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"','Sec-Ch-Ua-Mobile': '?0','Sec-Ch-Ua-Platform': '"macOS"','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-site','Sec-Gpc': '1','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',}
def display_header():
 os.system('clear')
 logging.info('\n'); logging.info('   ___        ____             _               '); logging.info('  / _ \\      / __ \\           (_)              '); logging.info(' | | | |_  _| |  | |_ __   ___ _ _ __ ___  ___ '); logging.info(' | | | \\ \\/ / |  | | \'_ \\ / _ \\ | \'__/ _ \\/ __|'); logging.info(' | |_| |>  <| |__| | | | |  __/ | | | (_) \\__ \\'); logging.info('  \\___//_/\\_\\\\____/|_| |_|\\___|_|_|  \\___/|___/'); logging.info('                                               '); logging.info('                                               ')
def send_sol(from_keypair, to_public_key, amount):
 connection = Client(DEVNET_URL, Confirmed)
 transaction = Transaction().add(transfer(TransferParams(from_pubkey=from_keypair.public_key,to_pubkey=to_public_key,lamports=int(amount * LAMPORTS_PER_SOL))))
 try:
  signature = connection.send_transaction(transaction, from_keypair, opts=TxOpts(skip_preflight=True, preflight_commitment=Confirmed))
  logging.info(f'Transaction confirmed with signature: {signature}')
 except Exception as e:
  logging.error(f'Error sending SOL: {e}')
def generate_random_addresses(count):
 return [Keypair.generate().public_key.to_base58().decode() for _ in range(count)]
def get_keypair_from_seed(seed_phrase):
 seed = bip39.mnemonic_to_seed(seed_phrase)
 derived_seed = BIP32Key.fromEntropy(seed).ExtendedKey()
 return Keypair.from_seed(derived_seed[:32])
def get_keypair_from_private_key(private_key):
 return Keypair.from_secret_key(base58.b58decode(private_key))
def get_keypair(private_key):
 decoded_private_key = base58.b58decode(private_key)
 return Keypair.from_secret_key(decoded_private_key)
def get_token(private_key):
 try:
  response = requests.get('https://odyssey-api-beta.sonic.game/auth/sonic/challenge',params={'wallet': str(get_keypair(private_key).public_key)},headers=HEADERS)
  data = response.json()
  sign = nacl.signing.SigningKey(get_keypair(private_key).secret_key).sign(data['data'])
  signature = base64.b64encode(sign.signature).decode()
  public_key = get_keypair(private_key).public_key
  encoded_public_key = base64.b64encode(public_key.to_bytes()).decode()
  response = requests.post('https://odyssey-api-beta.sonic.game/auth/sonic/authorize',headers=HEADERS,json={'address': str(public_key),'address_encoded': encoded_public_key,'signature': signature})
  return response.json()['data']['token']
 except Exception as e:
  logging.error(f"Error fetching token: {e}")
def get_profile(token):
 try:
  response = requests.get('https://odyssey-api-beta.sonic.game/user/rewards/info',headers={**HEADERS, 'Authorization': token})
  return response.json()['data']
 except Exception as e:
  logging.error(f"Error fetching profile: {e}")
def main():
 display_header()
 method = input('raveshe vasl shodan be wallet (0 VASE seed phrase, 1 VASE private key): ')
 if method == '0':
  with open('accounts.txt', 'r') as file:
   seed_phrases_or_keys = [line.strip() for line in file]
  if not isinstance(seed_phrases_or_keys, list) or len(seed_phrases_or_keys) == 0:
   raise ValueError('accounts.txt is not set correctly or is empty')
 elif method == '1':
  with open('privateKeys.txt', 'r') as file:
   seed_phrases_or_keys = [line.strip() for line in file]
  if not isinstance(seed_phrases_or_keys, list) or len(seed_phrases_or_keys) == 0:
   raise ValueError('privateKeys.txt is not set correctly or is empty')
 else:
  raise ValueError('Invalid input method selected')
 default_address_count = 100
 address_count_input = input(f'chandta tarakonesh bezane INAM bezan enter ? (pishfarz {default_address_count}): ')
 address_count = int(address_count_input) if address_count_input else default_address_count
 if address_count <= 0:
  raise ValueError('Invalid number of addresses specified')
 random_addresses = generate_random_addresses(address_count)
 try:
  connection = Client(DEVNET_URL, Confirmed)
  rent_exemption_amount = connection.get_minimum_balance_for_rent_exemption(0) / LAMPORTS_PER_SOL
  logging.info(f'Minimum balance for rent exemption: {rent_exemption_amount} SOL')
 except Exception as e:
  logging.error(f'Error fetching rent exemption amount: {e}')
  rent_exemption_amount = 0.001
 amount_to_send = 0
 while amount_to_send < rent_exemption_amount:
  amount_input = input('bezan enter ya edit kon (Pishfarz  0.001 SOL): ')
  amount_to_send = float(amount_input) if amount_input else 0.001
  if amount_to_send < rent_exemption_amount:
   logging.error(f'Invalid amount specified. The amount must be at least {rent_exemption_amount} SOL to avoid rent issues.')
   logging.info(f'Suggested amount to send: {max(0.001, rent_exemption_amount)} SOL')
 default_delay = 1000
 delay_input = input(f'bezan enter ya fasele beyne tarakonesh haro bede  (pishfarz {default_delay}ms): ')
 delay_between_tx = int(delay_input) if delay_input else default_delay
 for index, seed_or_key in enumerate(seed_phrases_or_keys):
  if method == '0':
   from_keypair = get_keypair_from_seed(seed_or_key)
  else:
   from_keypair = get_keypair_from_private_key(seed_or_key)
  logging.info(f'Sending SOL from account {index + 1}: {from_keypair.public_key}')
  for address in random_addresses:
   to_public_key = PublicKey(address)
   try:
    send_sol(from_keypair, to_public_key, amount_to_send)
    logging.info(f'Successfully sent {amount_to_send} SOL to {address}')
   except Exception as e:
    logging.error(f'Failed to send SOL to {address}: {e}')
   time.sleep(delay_between_tx / 1000)
if __name__ == "__main__":
 main()
