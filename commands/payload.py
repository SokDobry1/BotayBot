def payload_to_dict(data):
    text = '{"nodata": "None"}'
    if 'payload' in data:
        text = data['payload']
    prev_len = 0
    answer = dict()
    while True:
        s_key = text[prev_len:].find('"') + prev_len + 1
        if s_key > len(text): break
        e_key = text[s_key:].find('"') + s_key
        s_value = text[e_key + 1:].find('"') + (e_key + 1) + 1
        e_value = text[s_value:].find('"') + s_value
        prev_len += e_value + 2

        key, value = text[s_key:e_key], text[s_value:e_value]
        answer.update({key: value})
    return answer

#==========================================

def payload_to_str(dictionary):
    answer = r'{'
    for key, value in dictionary.items():
        answer += fr'\"{key}\": \"{value}\", '
    return answer[0:-2] + '}'

#=========================================

def get_element(data, name):
    ans = None
    payload = payload_to_dict(data)
    if name in payload:
        ans = payload[name]
    return ans









