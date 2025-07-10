## Instalation guide

first install git: https://git-scm.com/downloads

install python 3.9.12

on cmd run python --version

install vs code

git clone https://github.com/caetanovidal/challenge-api-fast-ap
run
 
pip install -r requirements.txt

install cuda  https://developer.nvidia.com/cuda-downloads?target_os=Windows

create an file named ".env"

add in ther you gpt KEY

OPENAI_API_KEY = "your-gpt-key-goes-here"



run 

uvicorn app:app --reload 