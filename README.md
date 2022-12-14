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

Inside CaddyProxy/conf directory, there is a default caddy.json,
which doesn't do anything useful yet. Change configuration with
`change.py` script. You can add as many mappings from domain to
address as you'd like. Provided example:

```
python change.py add "your.domain.com" "127.0.0.1:6000"
```

When you finish adding domain to address mappings, go back to parent directory,
where `docker-compose.yaml` file is located.
```
cd ..
```

And run it with:
```
docker-compose up -d
```

### Note:
You need docker and docker compose to run this.


### Reset file (change back to default json configuration):

```
python change.py reset
```

### Add reverse proxy with HTTPS:

```
python change.py add "domain.com" "127.0.0.1:9000"
```

# What is this intended for

This script is intended to ease deployment of a single or multiple HTTPS
(TLS) enabled websites with different domain names, on a single device (VPS).
