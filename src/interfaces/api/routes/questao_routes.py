from interfaces.api.controllers.questao_controller import router

def include_questao_routes(app):
    app.include_router(router)