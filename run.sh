fswatch -0 ./app/tests | xargs -0 -n 1 -I {} python ./app/main.py
