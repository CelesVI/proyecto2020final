def create_protocolo(filename):
    errors = []

    if filename == "":
        errors.append(f"El protocolo debe tener un nombre")
    else:
        if not "." in filename:
            errors.append(f"Archivos sin extensión no son aceptados")
        else:
            ext = filename.rsplit('.', 1)[1]
            if not (ext.upper() in {'PDF'}):
                errors.append(f"Archivo de extensión no permitida")

    result = len(errors) == 0

    return result, errors