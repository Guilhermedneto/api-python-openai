# Serviço para chamada à OpenAI
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        # Carrega variáveis do .env
        load_dotenv()
        endpoint = os.getenv("ENDPOINT_URL", "https://estudo-api.openai.azure.com/")
        deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-mini")
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.deployment = deployment
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=subscription_key,
            api_version="2025-01-01-preview",
        )


    def perguntar(self, pergunta: str) -> str:
        # Mantém método antigo para compatibilidade
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Você é um assistente de IA que ajuda as pessoas a encontrar informações."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": pergunta
                    }
                ]
            }
        ]
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=chat_prompt,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        return completion.choices[0].message.content if completion.choices else "Sem resposta."

    def perguntar_com_contexto(self, chat_prompt: list) -> str:
        """
        Recebe o prompt já montado (com histórico) e envia para OpenAI.
        """
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=chat_prompt,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        return completion.choices[0].message.content if completion.choices else "Sem resposta."
