#   Copyright 2022 Filip Strajnar
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import json
import sys


def add_reverse_proxy(from_domain: str, to_address: str):

    caddy_config = open("caddy.json", "r")
    entire_config = json.load(caddy_config)

    # Get certificate for new domain name
    entire_config["apps"]["tls"]["automation"]["policies"][0]["subjects"].append(
        from_domain
    )
    # Add reverse proxy handler
    entire_config["apps"]["http"]["servers"]["multi"]["routes"].append(
        {
            "match": [{"host": [from_domain]}],
            "handle": [
                {"handler": "reverse_proxy", "upstreams": [{"dial": to_address}]}
            ],
        }
    )

    caddy_config.close()
    # Write changes made to configuration file
    caddy_config = open("caddy.json", "w")
    json.dump(entire_config, caddy_config, indent=4)
    caddy_config.close()


def add_static_file_server(from_domain: str, from_path: str, root_path: str):
    caddy_config = open("caddy.json", "r")
    entire_config = json.load(caddy_config)

    # New static file server (handler)
    static_file_handler = [
        {
            "match": [{"host": [from_domain], "path": [from_path]}],
            "handle": [{"handler": "file_server", "root": root_path}],
        }
    ] + entire_config["apps"]["http"]["servers"]["multi"]["routes"]

    # Set new handler
    entire_config["apps"]["http"]["servers"]["multi"]["routes"] = static_file_handler

    caddy_config.close()
    # Write changes made to configuration file
    caddy_config = open("caddy.json", "w")
    json.dump(entire_config, caddy_config, indent=4)
    caddy_config.close()


def reset():
    # Reset to default configuration
    default_conf = """{
    "apps": {
        "tls": {
            "automation": {
                "policies": [
                    {
                        "subjects": [],
                        "issuers": [
                            {
                                "module": "acme"
                            }
                        ],
                        "renewal_window_ratio": 0.5,
                        "key_type": "p384"
                    }
                ]
            },
            "cache": {
                "capacity": 10000
            }
        },
        "http": {
            "http_port": 80,
            "https_port": 443,
            "servers": {
                "multi": {
                    "listen": [
                        ":443"
                    ],
                    "routes": []
                }
            }
        }
    }
}"""
    caddy_config = open("caddy.json", "w")
    caddy_config.write(default_conf)
    caddy_config.close()


if sys.argv[1] == "reset":
    reset()
elif sys.argv[1] == "add":
    # Example: python change.py add "my.domain.com" "127.0.0.1:5000"
    add_reverse_proxy(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "add-static":
    # Example: python change.py add-static "my.domain.com" "/static" "/static"
    # NOTE: with included docker-compose.yaml file, you should let the root path stay "/static"
    add_static_file_server(sys.argv[2], sys.argv[3], sys.argv[4])
else:
    print("Invalid command.")
