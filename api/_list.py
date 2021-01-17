from api.settings import *
import json
import requests

def test(name):
    def _test(data):
        return data
    return locals()[name]

def host(name):
    def reload_host(data):
        response = requests.post(
            f'https://{host}/api/v0/user/{username}/webapps/{domain_name}/reload/',
            headers={'Authorization': f'Token {token}'}
        )
        return {'status': 'OK'}

    def update_backup():
        return {'status': 'OK'}

    return locals()[name]

def bot(name):
    def technical_break(data):
        import message_handler
        message_handler.pls_wait = not message_handler.pls_wait
        return {'status': 'OK', 'answer': message_handler.pls_wait}

    return locals()[name]









