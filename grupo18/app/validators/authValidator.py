def update_config(params):
    required_params = ["email", "password"]

    errors = []

    for attribute in required_params:
        if attribute not in params:
            errors.append(f"El atributo '{attribute}' es requerido!")

        if not params.get(attribute):
            errors.append(f"El atributo '{attribute}' no puede estar vacío!")

    result = len(errors) == 0

    return result, errors