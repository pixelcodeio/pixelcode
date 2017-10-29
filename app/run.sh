fswatch -0 ./tests | xargs -0 -n 1 -I {} python main.py update
