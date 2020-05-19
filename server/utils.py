from settings import FORMAT, HEADER_LENGTH
import json

def encode_event(event_type:str, event_obj):
    obj_encoded = json.dumps(event_obj).encode(FORMAT)
    obj_encoded_len = len(obj_encoded)
    header = f"{event_type} {obj_encoded_len}".encode(FORMAT)
    header_padded = f"{header}<{HEADER_LENGTH}".encode(FORMAT)
    
    return (header_padded + obj_encoded).encode(FORMAT)

def parse_command(cmd_type, content):
    obj_dict = json.loads(content)
    return type(cmd_type, obj_dict)
