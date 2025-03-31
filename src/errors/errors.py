class ApiError(Exception):
    code = 422
    description = "Error en la API"

class MissingFieldsError(ApiError):
    code = 400
    description = "Faltan campos obligatorios"

class InvalidUUIDError(ApiError):
    code = 400
    description = "El id no es un valor string con formato UUID"

class InvalidSearchFieldsError(ApiError):
    code = 400
    description = "Alguno de los campos tiene un formato inválido"

class InvalidReasonFieldsError(ApiError):
    code = 400
    description = "El campo 'motivo' excede los 255 caracteres"

