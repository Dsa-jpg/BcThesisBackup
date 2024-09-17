import time
from datetime import datetime
from openai import OpenAI
from caching import cache_response, get_cached_response
from config import PROMPTMSG, OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

def log_time(message: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{current_time}] {message}")


def get_response(prompt: str) -> str:

    cached_response = get_cached_response(prompt)
    if cached_response:
        log_time("Cache hit.")
        return cached_response

    try:
        start_time = time.perf_counter()
        log_time("Starting OpenAI API call.")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPTMSG},
                {"role": "user", "content": prompt}
            ],
        )
        
        end_time = time.perf_counter() - start_time
        log_time(f"OpenAI API call completed. Response time: {end_time:.2f} seconds")
        
        result = response.choices[0].message.content
        # Cache the response
        cache_response(prompt, result)


        return result
    
    except Exception as e:
        log_time(f"Error during OpenAI API call: {str(e)}")
        return str(e)
    

async def get_response_stream(prompt: str):

    
    try:
        # Použití streamu od OpenAI
        start_time = time.perf_counter()
        log_time("Starting OpenAI API streaming call.")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPTMSG},
                {"role": "user", "content": prompt}
            ],
            stream=True  # Povolení streamování
        )
        
        end_time = time.perf_counter() - start_time
        log_time(f"OpenAI streaming call completed. Response time: {end_time:.2f} seconds")
        
        # Vrací postupné části odpovědi
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    except Exception as e:
        log_time(f"Error during OpenAI streaming call: {str(e)}")
        yield str(e)



async def get_response_stream_(prompt: str):
    # Check if response is in cache
    cached_response = get_cached_response(prompt)
    if cached_response:
        log_time("Cache hit.")
        yield cached_response
        return

    try:
        # Použití streamu od OpenAI
        start_time = time.perf_counter()
        log_time("Starting OpenAI API streaming call.")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPTMSG},
                {"role": "user", "content": prompt}
            ],
            stream=True  # Povolení streamování
        )
        
        # Sestavení celé odpovědi
        full_response = ""
        
        # Vrací postupné části odpovědi
        for chunk in response:
            if chunk.choices[0].delta.content:
                part = chunk.choices[0].delta.content
                full_response += part
                yield part
        
        # Uložení celé odpovědi do cache
        cache_response(prompt, full_response)
        
        end_time = time.perf_counter() - start_time
        log_time(f"OpenAI streaming call completed. Response time: {end_time:.2f} seconds")

    except Exception as e:
        log_time(f"Error during OpenAI streaming call: {str(e)}")
        yield str(e)


"""
def get_response_test(prompt: str) -> str:

    
    
    import requests

    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Jsi humanoidní robot jménem NAO. Tvůj domov je v Českých Budějovicích, konkrétně na Jihočeské Univerzitě v koleji K3. Tvůj věk je 5 let, což pro robota jako jsi ty znamená, že jsi v plné síle svých schopností."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
    }
    start_time = time.perf_counter()
    response = requests.post(url, headers=headers, json=data)
    api_time = time.perf_counter() - start_time
    if response.status_code == 200:
        print(f"OpenAI response time: {api_time:.2f} seconds")
        return response.json()['choices'][0]['message']['content']
    else:
        return response.json()


"""

    