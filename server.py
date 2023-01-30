import os
import http.server
import socketserver

from http import HTTPStatus

import uuid
import random
import json
import datetime

def generate_json():
    data = {
        "id": str(uuid.uuid4()),
        "timestampStarted": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat() + "Z",
        "timestampEnded": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat() + "Z",
        # "metric": random.choice(["M_REACHABILITY", "M_LATENCY", "M_BANDWIDTH", "M_PACKET_LOSS", "M_TCP_RETRANSMISSIONS"]),
        "metric": "M_REACHABILITY",

        "causes": [
            {
                "id": str(uuid.uuid4()),
                "type": random.choice(["ISP", "CDN", "CLOUD"]),
                "sourceAsns": [
                    str(random.randint(1000, 9000))
                ],
                "h3Indexes": [
                    str(uuid.uuid4())[:15]
                ],
                #limit network_id to 202 - 210
                "networkIds": [
                    str(random.randint(200, 210)),
                    str(random.randint(202, 210)),
                    str(random.randint(202, 210))
                ],
                "causeAsn": str(random.randint(1000, 9000)),
                "timestampStarted": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat() + "Z",
                "measurementCount": str(random.randint(0, 50)),
                "alertsMatched": [
                    {
                        "id": str(uuid.uuid4()),
                        "timestampStarted": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat() + "Z",
                        "timestampEnded": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat() + "Z",
                        "sourceAsn": str(random.randint(1000, 9000)),
                        "sourceGeospatialH3Index": str(uuid.uuid4())[:15],
                        #change network_id to 202-210
                        "destinationNetworkId": str(random.randint(202, 210)),
                        #"metric": random.choice(["M_REACHABILITY", "M_LATENCY", "M_BANDWIDTH", "M_PACKET_LOSS", "M_TCP_RETRANSMISSIONS"]),
                        "metric": random.choice(["M_REACHABILITY"]),
                        "value": random.uniform(0, 80),
                        #"valueUnit": random.choice(["ms", "bps", "pct"]),
                        "valueUnit": "pct",
                        #"valueBaseline": random.uniform(0, 1000),
                        "valueBaseline": "97",
                        "measurementCount": str(random.randint(0, 50))
                    }
                ]
            }
        ]
    }

    return data

# Generate 10 additional records
records = [generate_json() for i in range(10)]

# Write records to a JSON
# print(records)
# print(json.dumps(records, indent = 3))

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
    # Should http headers be here?
        self.end_headers()
        # msg = 'Hello! you requested %s' % (self.path)
        msg = (json.dumps(records, indent = 3))
        self.wfile.write(msg.encode())
        r = requests.get('https://x8ki-letl-twmt.n7.xano.io/api:qTxuLGUC/my_first_endpoint')
        self.wfile.write(r.encode())
        

port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
