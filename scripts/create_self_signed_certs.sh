openssl genrsa -out private-key.pem 2048
python3 create_ssl_cnf.py
openssl req -new -x509 -days 365 -key private-key.pem -config configuration.cnf -out certificate.pem
mv *.pem ../keys/
rm configuration.cnf
