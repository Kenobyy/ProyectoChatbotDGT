
cache = {}

def get_ddl(table, db_chain):

    # Verificar si el resultado ya está en caché
    if table in cache:
        return cache[table]

    # Si no está en caché, realizar la consulta a la base de datos
    result = db_chain(f'Describe table {table}')

    # Almacenar en caché el resultado
    cache[table] = result['intermediate_steps'][0]['table_info']

    return cache[table]
