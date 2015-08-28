base_cnf="""[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = {state}
L = {city}
O = {org}
CN = {skill}

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @subject_alternate_names

[subject_alternate_names]
DNS.1 = {DNS}
"""


def create_cnf_from_input():
    print ("Creating config file... info needed: state, city, organization name and DNS")
    state = input("> Which state are you in?\n")
    city = input("> Which city?\n")
    org = input("> What is the name of your organization?\n")
    skill = input("> What is the name of your alexa skill?\n")
    dns = input("> What is your DNS?\n")
    with open("configuration.cnf", 'w') as cnfile:
        print(base_cnf.format(state=state.strip(), city=city.strip(),
                              org=org.strip(), skill=skill.strip(), DNS=dns.strip()),
              file=cnfile)
    print("Cleaning up configuration.cnf file, moving private key and certificate to ../keys folder")

create_cnf_from_input()
