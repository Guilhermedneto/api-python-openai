from application.services.openai_service import OpenAIService

if __name__ == "__main__":
    service = OpenAIService()
    pergunta = "Qual é a capital do Brasil?"
    resposta = service.perguntar(pergunta)
    print(f"Pergunta: {pergunta}")
    print(f"Resposta: {resposta}")
