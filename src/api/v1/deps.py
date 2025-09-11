from fastapi import Request


def get_easyclinic(request: Request):
    """
    Возвращает singleton-клиент из app.state, созданный в lifespan.
    """
    return request.app.state.ec