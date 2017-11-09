#!/usr/bin/env python

import charm.proto.hex_pb_signed_pb2
import charm.proto.hex_pb_names_pb2
import charm.proto.hex_pb_versions_pb2
import rsa
import gzip
import requests
import os.path
import cPickle
import time

UPSTREAM_HEX_URL="https://repo.hex.pm"
RESOURCE_DIR="resources"
RESOURCES=["names", "versions"]

class SignatureMatchException(Exception):
    """Exception when the RSA signature for a resource doesn't match the public key."""

def make_upstream_hex_url(resource):
    return UPSTREAM_HEX_URL + "/" + resource

def fetch_resource(url):
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        return r
    else:
        r.raise_for_status()

def make_resource_path(filename, loc=RESOURCE_DIR):
    if os.path.exists(loc):
        return os.path.join(loc, filename)
    else:
        raise IOError("{0} doesn't seem to exist".format(loc))

def save_resource(r, filename, loc=RESOURCE_DIR):
    fn = make_resource_path(filename, loc)
    print "Saving {0} to {1}".format(filename, fn)
    with open(fn, "wb") as f:
        f.write(r.content)

def maybe_get_resources():
    for res in RESOURCES:
        try:
            t = os.path.getmtime(make_resource_path(res))
            if ( time.time() - t ) > 86400:
                get_resource(res)
            else:
                print "Skipping resource '{0}' because it's still fresh".format(res)
        except OSError:
            # If we get an OSError that should mean the file doesn't exist yet,
            # so let's get it.
            get_resource(res)

def get_resource(res):
        url = make_upstream_hex_url(res)
        r = fetch_resource(url)
        save_resource(r, res)

maybe_get_resources()

snames = charm.proto.hex_pb_signed_pb2.Signed()
sver = charm.proto.hex_pb_signed_pb2.Signed()

with gzip.open(make_resource_path("names"), "rb") as f:
    snames.ParseFromString(f.read())

with gzip.open(make_resource_path("versions"), "rb") as f:
    sver.ParseFromString(f.read())

hex_pubkey_contents = None 
with open(make_resource_path("hex_pub.pem", "keys"), "rb") as f:
    hex_pubkey_contents = f.read()

hex_pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(hex_pubkey_contents)

if rsa.verify(snames.payload, snames.signature, hex_pubkey):
    print "names resource verified"
else:
    raise SignatureMatchException("The signature for the names resource does not match")

if rsa.verify(sver.payload, sver.signature, hex_pubkey):
    print "versions resource verified"
else:
    raise SignatureMatchException("The signature for the versions resource does not match")

n = charm.proto.hex_pb_names_pb2.Names()
n.ParseFromString(snames.payload)

hex_data = {}
for p in n.packages:
    hex_data[p.name] = {}
    hex_data[p.name]['versions'] = {}

v = charm.proto.hex_pb_versions_pb2.Versions()
v.ParseFromString(sver.payload)

for p in v.packages:
    if p.retired:
        hex_data[p.name]['retired'] = p.retired
    if p.namespace:
        hex_data[p.name]['namespace'] = p.namespace

    for v in p.versions:
        hex_data[p.name]['versions'][v] = True 

with open(os.path.join(RESOURCE_DIR, "hex_data.pkl"), "wb") as f:
    cPickle.dump(hex_data, f)

print "Wrote hex_data"
