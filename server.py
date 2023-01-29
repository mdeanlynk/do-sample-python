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
        "metric": random.choice(["M_LATENCY", "M_BANDWIDTH", "M_PACKET_LOSS"]),
        "causes": [
            {
                "id": str(uuid.uuid4()),
                "type": random.choice(["ECT_ISP", "ECT_PEERING", "ECT_INTERNAL"]),
                "sourceAsns": [
                    str(random.randint(1000, 9000))
                ],
                "h3Indexes": [
                    str(uuid.uuid4())[:15]
                ],
                "networkIds": [
                    str(random.randint(10000, 99999)),
                    str(random.randint(10000, 99999)),
                    str(random.randint(10000, 99999))
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
                        "destinationNetworkId": str(random.randint(10000, 99999)),
                        "metric": random.choice(["M_LATENCY", "M_BANDWIDTH", "M_PACKET_LOSS"]),
                        "value": random.uniform(0, 1000),
                        "valueUnit": random.choice(["ms", "bps", "pct"]),
                        "valueBaseline": random.uniform(0, 1000),
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
        self.end_headers()
        # msg = 'Hello! you requested %s' % (self.path)
        msg = (json.dumps(records, indent = 3))
        self.wfile.write(msg.encode())


port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
