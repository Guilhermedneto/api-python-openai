class CreateQuestaoCommandValidation:
    def validate(self, command):
        if not command.texto_pergunta or not command.texto_pergunta.strip():
            raise ValueError("A pergunta não pode ser vazia.")
        if len(command.texto_pergunta.strip()) < 3:
            raise ValueError("A pergunta deve ter pelo menos 3 caracteres.")
        if not command.usuario or not command.usuario.strip():
            raise ValueError("Usuário é obrigatório.")
        if len(command.usuario.strip()) < 3:
            raise ValueError("Usuário deve ter pelo menos 3 caracteres.")
        if len(command.usuario.strip()) > 100:
            raise ValueError("Usuário muito longo (máximo 100 caracteres).")
        # texto_resposta é ignorado na validação, pois é preenchido pelo sistema
