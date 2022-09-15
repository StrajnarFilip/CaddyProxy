# How to use

To use this script, clone this repository with:

```
git clone https://github.com/StrajnarFilip/CaddyProxy.git
```

Once cloned, change directory:
```
cd CaddyProxy
```

In this directory, `docker-compose.yaml` file is located.
To actually configure the reverse proxy, change directory once again:

```
cd conf
```

Inside CaddyProxy/conf directory, there is an default caddy.json,
which doesn't do anything useful yet. Change configuration with
`change.py` script.


### Reset file (change back to default json configuration):

```
python change.py reset
```

### Add reverse proxy with HTTPS:

```
python change.py add "domain.com" "127.0.0.1:9000"
```