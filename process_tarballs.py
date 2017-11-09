import tempfile
from erl_terms import decode
import os.path
import tarfile
import pprint
import shutil

TARBALL_DIR='tarballs'

def make_tarball_path(fname, loc=TARBALL_DIR):
    return os.path.join(loc, fname)

tmpdir = tempfile.mkdtemp()

with tarfile.open(make_tarball_path("gisla-1.0.0.tar")) as tf:
    tf.extractall(path=tmpdir)

metadata = None
with open(make_tarball_path("metadata.config", tmpdir), "rb") as f:
    metadata = decode(f.read())

pprint.pprint(metadata)

shutil.rmtree(tmpdir)
