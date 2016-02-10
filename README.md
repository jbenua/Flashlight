# Flashlight
TCP flashlight client


# Server
Run server: `python3 server.py`. You can specify port by `--port=value`.

# Client
Run client: `python3 client.py`
You can specify port by `--port=value` and choose console-only view: `--console=True`.
If you choose web-view (default value for `console`), after starting the client go to `127.0.0.1:8888`

# Commands
When server is running and client is connected, send some commands to client from server. Use
`on`, `off`, something like `color 200 150 3` or byte sequence.

# Other
You can also run tests, using [green](https://github.com/CleanCut/green), for example
