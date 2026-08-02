import uuid


def generate_id():
    uniq_obj = uuid.uuid4()
    return str(uniq_obj)


