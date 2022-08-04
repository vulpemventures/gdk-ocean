# gdk-ocean

gdk-ocean is a Liquid wallet running on a gRPC server. It implements the [ocean API](https://github.com/vulpemventures/ocean)

# Usage

## Run gdk-ocean locally

The current version of gdk-ocean uses Python 3.9

__the first time you run the program, you have to set up the virtual env with all dependencies.__

Init the submodules:
```
git submodule update --init --recursive
```

And copy the stubs:
```
make stubs
```

Create virtual env (it needs Python 3.9 installed)
```
make env
```

Then, activate the env and install the `requirements.txt` deps.
```
source venv/bin/activate
make deps
```

At any moment, you can leave the venv with `deactivate`.

Now you can run the server in any Python 3.9 environmnent:
```
make run
```
By default, the server is running on port 50051.

## Run gdk-ocean in a Docker container

Init the submodules and copy the proto stubs:
```
git submodule update --init --recursive
make stubs
```

Build the image:
```bash
docker build -t gdk-ocean . # -t is the image name
```

Run a container:
```bash
docker run gdk-ocean 
```

Once the container is running, you can request it via the exposed port 50051.

## CLI

You can communicate with gdk-ocean using the `cli.py` script. It must be run by python3.9.

In your virtual enviroment, install the CLI dependencies:
```bash
pip install -r requirements_cli.txt
```

> if you are running the server in a container or if u don't want to mix CLI & server env, you can create venv with: `python3.9 -m venv venv_cli`

The CLI can connect to a gdk-ocean server using `--host` and `--port` options
```bash
python cli.py --address 0.0.0.0:8080 <command>
python cli.py <command> # if not set, cli.py requests localhost:50051 by default
``` 

Try to create your wallet using the cli:
```bash
python cli.py genseed # write down your secret words!
python cli.py create -m "<seed>" -p "<password>"
```

You can print the list of commands by running `python cli.py --help`. Any command help message can be printed by running `python cli.py <command> --help`.
