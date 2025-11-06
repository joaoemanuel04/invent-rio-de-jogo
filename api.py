# -*- coding: utf-8 -*-
import requests
import json
import base64
from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad
import dados # Importamos para sincronizar o usuário local

from dotenv import load_dotenv
load_dotenv()

# --- URLs REAIS FORNECIDAS ---
API_URL_SEM_SEGURANCA = os.environ.get("API_URL_SEM_SEGURANCA")
API_URL_COM_SEGURANCA = os.environ.get("API_URL_COM_SEGURANCA")
AES_KEY_STRING = os.environ.get("AES_KEY")
if not API_URL_SEM_SEGURANCA or not API_URL_COM_SEGURANCA or not AES_KEY_STRING:
    print("[ERRO FATAL] Variáveis de ambiente (API_URL_*, AES_KEY) não definidas.")
    # Em um app real, você não continuaria a execução aqui
    AES_KEY = None
else:
    # Converte a chave string para bytes
    AES_KEY = AES_KEY_STRING.encode('utf-8')

def encrypt_password_aes(password):
    """
    Criptografa a senha usando AES-128 (ECB) e codifica em Base64.
    """
    if not AES_KEY:
        print("Erro: Chave AES não foi carregada.")
        return None
        
    try:
        # ... (O resto da sua função de criptografia) ...
        print(f"[API] Criptografando senha...")
        
        cipher = AES.new(AES_KEY, AES.MODE_ECB)
        password_bytes = password.encode('utf-8')
        padded_password = pad(password_bytes, AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_password)
        encrypted_base64_string = base64.b64encode(encrypted_bytes).decode('utf-8')
        
        print("[API] Senha criptografada e codificada em Base64.")
        return encrypted_base64_string
    except Exception as e:
        print(f"Erro ao criptografar: {e}")
        return None

# --- FUNÇÃO PARA O BOTÃO SEGURO ---
def login_api_segura(username, password):
    """
    Executa o login contra a API segura (syncjava2.php) com criptografia.
    """
    if not username or not password:
        return None, "Erro: Usuário e senha não podem estar vazios."
        
    encrypted_pass = encrypt_password_aes(password)
    if not encrypted_pass:
        return None, "Erro: Falha interna ao criptografar a senha."
    
    if not API_URL_COM_SEGURANCA:
        return None, "Erro: URL da API Segura não configurada."
        
    payload = {
        "usuario": username,
        "senha": encrypted_pass
    }
    
    try:
        # --- MENSAGEM NO TERMINAL ---
        print(f"[API] Tentando login em API SEGURA para: {username}")
        response = requests.post(API_URL_COM_SEGURANCA, data=payload, timeout=10)
        resposta_texto = response.text.strip()
        
        if response.status_code == 200 and "login realizado com sucesso" in resposta_texto.lower():
            # SUCESSO
            user_id_local = dados.get_or_create_user_id_local(username)
            if user_id_local:
                return user_id_local, f"API Segura (HTTP {response.status_code}): {resposta_texto}"
            else:
                return None, f"API Segura (HTTP {response.status_code}): Login OK, mas falha ao criar usuário local."
        else:
            # FALHA
            return None, f"API Segura (HTTP {response.status_code}): {resposta_texto}"

    except requests.exceptions.RequestException as e:
        return None, f"Erro de Conexão (API Segura): {e}"

# --- FUNÇÃO PARA O BOTÃO INSEGURO ---
def login_api_insegura(username, password):
    """
    Executa o login contra a API sem segurança (syncjava.php) sem criptografia.
    """
    if not username or not password:
        return None, "Erro: Usuário e senha não podem estar vazios."
    
    if not API_URL_SEM_SEGURANCA:
        return None, "Erro: URL da API Insegura não configurada."

    payload = {
        "usuario": username,
        "senha": password 
    }

    try:
        # --- MENSAGEM NO TERMINAL ---
        print(f"[API] Tentando login em API INSEGURA para: {username}")
        response = requests.post(API_URL_SEM_SEGURANCA, data=payload, timeout=10)
        resposta_texto = response.text.strip() 

        if response.status_code == 200 and "login realizado com sucesso" in resposta_texto.lower():
            # SUCESSO (Resposta com Texto)
            user_id_local = dados.get_or_create_user_id_local(username)
            if user_id_local:
                return user_id_local, f"API Insegura (HTTP {response.status_code}): {resposta_texto}"
            else:
                return None, f"API Insegura (HTTP {response.status_code}): Login OK, mas falha ao criar usuário local."
        
        elif response.status_code == 200:
            try:
                # SUCESSO (Resposta com JSON)
                data = response.json()
                if data.get("status") == "OK":
                    user_id_local = dados.get_or_create_user_id_local(username)
                    if user_id_local:
                        return user_id_local, f"API Insegura (HTTP {response.status_code}): {data.get('msg')}"
                    else:
                        return None, f"API Insegura (HTTP {response.status_code}): Login OK, mas falha ao criar usuário local."
                else:
                    return None, f"API Insegura (HTTP {response.status_code}): {data.get('msg', 'Resposta de erro da API')}"
            except json.JSONDecodeError:
                # ERRO (Texto inesperado, ex: "Conexao perdida!")
                return None, f"API Insegura (HTTP {response.status_code}): {resposta_texto}"
        
        else:
            # ERRO (Status code != 200)
            return None, f"Erro do servidor (API Insegura): {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return None, f"Erro de Conexão (API Insegura): {e}"