# gdk-ocean

gdk-ocean is a Liquid wallet running on a gRPC server. It implements the [ocean API](https://github.com/vulpemventures/ocean)

# Usage

## Server

The current version of gdk-ocean uses Python 3.9, see `requirements.txt` for dependencies.

Run the server in any Python 3.9 environmnent:
```
make run
```

## CLI

You can communicate with gdk-ocean using the `cli.py` script. 

### Development

Create virtual env (need Python 3.9 installed)
```
make env
```

Then, activate the env and install the dependencies.
```
source venv/bin/activate
make deps
```

Run the gdk-ocean instance
```
make run
```