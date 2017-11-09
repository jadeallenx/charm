Generate keys using OpenSSL
===========================
Hex repositories are required to sign their resource files. When you set up a charm repository, you will need to generate
an RSA keypair to sign your resources.

     openssl genrsa -out privatekey.pem 2048
     openssl rsa -in privatekey.pem -pubout -out publickey.pem

**NOTE**: Do not share/distribute/check in the private key. This is the secret which guarantees the signatures
on resources are valid.  You must share/distribute/check in the public key though.  That's what other users will
download to validate the resources they get from your charm installation.
