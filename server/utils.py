from settings import FORMAT, HEADER_LENGTH
import jsonpickle as jp

def encode_event(event_type:str, event_obj):
    obj_encoded = jp.encode(event_obj).encode(FORMAT)
    obj_encoded_len = len(obj_encoded)
    header = f"{event_type} LENGTH:{obj_encoded_len}".encode(FORMAT)
    header_padded = f"{header}<{HEADER_LENGTH}".encode(FORMAT)
    
    return (header_padded + obj_encoded).encode(FORMAT)