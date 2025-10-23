


from domain.exceptions.base_exception import DomainEntityNotFoundException


class QuestaoNaoEncontradaException(DomainEntityNotFoundException):
    def __init__(self, questao_id: str):
        super().__init__(f"Questão com ID {questao_id} não encontrada.")
        

