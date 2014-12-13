
'''
  Chequea que todos los campos pasados en la lista fields existan
  Retorna una lista con los campos que no existen
'''
def checkRequiredFields(message,fields):
  errorFields = []
  for f in fields:
    if f not in message:
      errorFields.append(f)

  return errorFields
  
