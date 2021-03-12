def create_issue(params):
    required_params = ['email', 'description', 'category_id', 'status_id']

    errores = []

    for attribute in required_params:
        if attribute not in params:
            errores.append(f"El atributo '(attribute)' es requerido")

        if not params.get(attribute):
            errores.append(f"El atributo '(attribute)' no puede estar vacío")

    result = len(errores) == 0

    return result, errores