Contains python3 scripts to help setup an inital codebase for creating an alexa app in python.
---
generate_intent_schema.py 
---
Generates a intent_schema.json file by prompting the user

---
generate_training_data.py
---

Uses an intent_schema as input and helps a user generate sample utterances for training the model.

---
create_self_signed_certs.sh
---
Uses OpenSSL and command line prompts to take the user through the process of generating a private key and self signed certificate.

---
create_ssl_cnf.py
---
Utility function used to quickly create a .cnf file - used by create_self_signed_certs.sh
