fswatch -0 ./exports | xargs -0 -n 1 -I {} python main.py
