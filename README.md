# ffxiv_friend_tracker

    Go here setup account for api key https://xivapi.com/
    git clone https://github.com/xivapi/xivapi-py

    Setup environment
        mkdir .venv
        python3 -m pip install pipenv
        python3 -m pipenv install
        python3 -m pip install -r $PATH/xivapi-py/requirements.txt
        python3 -m pip install $PATH/xivapi-py


    Next you can run these commands
        python collect_data.py
        python generate_html.py

    Will generate a static index.html you can share
