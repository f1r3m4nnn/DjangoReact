import json

def attemptJSONDeserialize(data, expected_type=None):
    """
    Tenta deserializar um objeto JSON e verifica se o tipo do objeto deserializado
    corresponde ao esperado.

    :param data: O objeto JSON a ser deserializado.
    :param expected_type: O tipo esperado do objeto deserializado.
    :return: O objeto deserializado.
    :raises ValueError: Se o tipo do objeto não corresponder ao esperado.
    """
    try:
        data = json.loads(data)
    except (TypeError, json.decoder.JSONDecodeError):
        pass

    if expected_type is not None and not isinstance(data, expected_type):
        raise ValueError(
            f"Esperado um {expected_type.__name__} após a deserialização, "
            f"mas retornou um {type(data).__name__} ao invés."
        )

    return data

