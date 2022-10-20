import os

def get_env_var(varname: str):
    if os.environ.get(varname) is not None:
        return os.environ[varname]
    else:
        from dotenv import load_dotenv
        load_dotenv()
        return os.environ[varname]
