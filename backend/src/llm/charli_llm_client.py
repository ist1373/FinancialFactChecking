import requests
import time
import urllib
from src.core.config import settings


class CharliLLMClient:
    """A general client for calling LLM APIs."""

    def __init__(self, max_retries: int = 3):
        """
        Initializes the LLM client.
        
        :param host_url: The URL of the LLM API.
        :param host_endpoint: The end point of the LLM call.
        :param max_retries: Number of retry attempts on failure.
        """
        self.host_url = settings.LLM_HOST_URL
        self.host_endpoint = settings.LLM_HOST_ENDPOINT
        self.max_retries = max_retries
    
    def format_input(self, system_prompt: str, user_prompt: str)-> dict:
        prompt =  f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        payload = {"text_input":prompt,"parameters": {"stream": False, "temperature": 0, "max_tokens": 8000, "stop": "<|eot_id|>"}}
        return payload

    def call(self, payload: dict) -> str:
        """
        Makes a request to the LLM API.
        :param payload: A dictionary containing the request payload.
        :return: A dictionary containing the LLM response.
        """

        attempt = 0
        while attempt < self.max_retries:
            try:
                endpoint = urllib.parse.urljoin(self.host_url, self.host_endpoint)
                result = requests.post(endpoint, json=payload)
                result.raise_for_status()
                results = result.json()["text_output"]
                return results
            except requests.exceptions.RequestException as e:
                print(f"Error calling LLM (attempt {attempt + 1}): {e}")
                attempt += 1
                time.sleep(2 ** attempt)  

        return {"error": "Failed to fetch response from LLM after retries"}


llm_client = CharliLLMClient()  

def get_llm_client() -> CharliLLMClient:
    return llm_client