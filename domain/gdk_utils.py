import greenaddress as gdk
import json

def make_session(network: str) -> gdk.Session:
    return gdk.Session({'name': network})

def gdk_resolve(auth_handler):
    # Processes and handles the state of calls that need authentication.
    # The authentication process works as a state machine and may require input to progress in case of 2FA enabled.
    # this implementation raises an error in case of 2FA enabled.
    while True:
        status = gdk.auth_handler_get_status(auth_handler)
        status = json.loads(status)
        state = status['status']
        if state == 'error':
            raise RuntimeError(f'\nAn error occurred authenticating the call: {status}')
        if state == 'done':
            return status['result']
        elif state == 'call':
            gdk.auth_handler_call(auth_handler)
        else:
            raise RuntimeError(f'\nUnknown state: {state} in auth_handler')

   