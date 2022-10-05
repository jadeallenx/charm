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
    def is_within_directory(directory, target):
        
        abs_directory = os.path.abspath(directory)
        abs_target = os.path.abspath(target)
    
        prefix = os.path.commonprefix([abs_directory, abs_target])
        
        return prefix == abs_directory
    
    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    
        for member in tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not is_within_directory(path, member_path):
                raise Exception("Attempted Path Traversal in Tar File")
    
        tar.extractall(path, members, numeric_owner=numeric_owner) 
        
    
    safe_extract(tf, path=tmpdir)

metadata = None
with open(make_tarball_path("metadata.config", tmpdir), "rb") as f:
    metadata = decode(f.read())

pprint.pprint(metadata)

shutil.rmtree(tmpdir)
