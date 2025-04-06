import requests
import datetime
import shelve
from typing import Dict, List
import os
import pathlib
CACHE_FILE = "token_cache"
import base64


def generate_prompt(topic: str, instrumental: bool, model_public_name: str, bearer_token: str = None) -> dict:
    """
    Calls the Riffusion API to generate a prompt.

    Args:
        topic (str): The topic for the generation.
        instrumental (bool): Whether to include instrumental.
        model_public_name (str): The name of the model to use.

    Returns:
        dict: The response from the API.
    """
    # Set up the headers
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "authorization": "Bearer " + (bearer_token if bearer_token else ""),
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.riffusion.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.riffusion.com/",
        "sec-ch-ua": "\"Brave\";v=\"135\";\"Not-A.Brand\";v=\"8\";\"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    # Set up the data
    data = {
        "topic": topic,
        "instrumental": instrumental,
        "model_public_name": model_public_name
    }

    try:
        response = requests.post(
            url="https://wb.riffusion.com/generate/prompt",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def main():
    """
    Main function to run the script.
    """
    # Example usage
    topic = "A beautiful sunset"
    instrumental = False
    model_public_name = "FUZZ-0.8"
    bearer_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6ImZrT3BsR2t1Y081Y21BQjIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2hndHB6dWtlem9keHJnbWZobHZ5LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJiNDIxMGFjNS05YjdkLTRjZjAtYWY3NC03OTBkNTZkMmJiYWIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzQzODkwMzkwLCJpYXQiOjE3NDM4ODg1OTAsImVtYWlsIjoiYXBwYWRvb2Fwb29ydmFAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJ1c2VyX21ldGFkYXRhIjp7ImF2YXRhcl91cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLMWFlSjF6dnJOUnRNMDJ3YVNPUUNXS3pGcDliOTJ2S0ZseTk5dXRjWUtGUHJlcTJ0cT1zOTYtYyIsImVtYWlsIjoiYXBwYWRvb2Fwb29ydmFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6IkFwb29ydmEgU3Jpbml2YXMgQXBwYWRvbyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJBcG9vcnZhIFNyaW5pdmFzIEFwcGFkb28iLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLMWFlSjF6dnJOUnRNMDJ3YVNPUUNXS3pGcDliOTJ2S0ZseTk5dXRjWUtGUHJlcTJ0cT1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTExNjk5MzExMjk4NjQ5NzA4MTg0Iiwic3ViIjoiMTExNjk5MzExMjk4NjQ5NzA4MTg0In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoib2F1dGgiLCJ0aW1lc3RhbXAiOjE3NDIwNjcwNzN9XSwic2Vzc2lvbl9pZCI6IjQ2NTdlNGYyLTVhMTctNGMyNC05MWYzLWEzMDQyZTY1YjY2ZiIsImlzX2Fub255bW91cyI6ZmFsc2V9.QVQ5XYP_plpQCN0Y1PQZj5QVaTgmFSue18xElEVOwic"

    prompt_response = generate_prompt(topic, instrumental, model_public_name, bearer_token)

    if prompt_response:
        print("Prompt generated successfully:")
        print(prompt_response)
    else:
        print("Failed to generate prompt.")


def get_token(refresh_token: str) -> dict:
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhndHB6dWtlem9keHJnbWZobHZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcxODc0MTUsImV4cCI6MjA1Mjc2MzQxNX0.Euec5ChPLivlNRbiaGcyLHu-EP_6qYxcIUxV7tiXVpw"
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "apikey": api_key,
        "authorization": f"Bearer {api_key}",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.riffusion.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.riffusion.com/",
        "sec-ch-ua": "\"Brave\";v=\"135\";\"Not-A.Brand\";v=\"8\";\"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-client-info": "supabase-ssr/0.5.2",
        "x-supabase-api-version": "2024-01-01"
    }

    # Set up the data
    data = {
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(
            url="https://api.riffusion.com/auth/v1/token?grant_type=refresh_token",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_cached_token(refresh_token: str) -> Dict:
    key = f"token::"
    with shelve.open(CACHE_FILE) as cache:
        if key in cache:
            cached = cache[key]

            if cached and cached["expires_at"] > datetime.datetime.now().timestamp():
                return cached  # Token is still valid

        # Token is missing or expired; refresh it
        new_token = get_token(refresh_token)
        cache[f"token::"] = new_token
        return new_token


def token_rotater(initial_refresh_token: str):
    """
    Rotate the refresh token and return the new token.
    """
    refresh_token = initial_refresh_token

    def rotate():
        nonlocal refresh_token
        token = get_cached_token(refresh_token)
        refresh_token = token["refresh_token"]
        return token

    return rotate


def base64_decode(data: str) -> bytes:
    """
    Decode a base64 string.

    Args:
        data (str): The base64 string to decode.

    Returns:
        bytes: The decoded bytes.
    """
    return base64.b64decode(data)


def get_job_status(job_id, bearer_token):
    # https://wb.riffusion.com/generate/status/{job_id}
    url = f"https://wb.riffusion.com/generate/status/{job_id}"

    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "authorization": "Bearer " + (bearer_token if bearer_token else ""),
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.riffusion.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.riffusion.com/",
        "sec-ch-ua": "\"Brave\";v=\"135\";\"Not-A.Brand\";v=\"8\";\"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_generations(riff_ids: List[str], bearer_token: str) ->  dict:
    # Set up the headers
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "authorization": "Bearer " + (bearer_token if bearer_token else ""),
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.riffusion.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.riffusion.com/",
        "sec-ch-ua": "\"Brave\";v=\"135\";\"Not-A.Brand\";v=\"8\";\"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    # Set up the data
    data = {
        "riff_ids": riff_ids
    }

    try:
        response = requests.post(
            url="https://wb.riffusion.com/v2/generations",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # open test.txt

    print(get_generations(["368a4725-e6cb-4749-8116-14cad90b31a1"], bearer_token=bearer_token)['generations'][0]['audio_url'])


