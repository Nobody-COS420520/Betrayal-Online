import os

def main():

    # You need to have python installed and python available in your path.
    # You also need to have the python script dir in your path because
    # "python -m pgzrun betrayal.py" works but breaks Pygame Zero 
    
    # it is "pip install -r requirements.txt" instead of
    # "python -m pip install -r requirements.txt" to enforce this
    
    os.system("pip install -r requirements.txt")
    os.system("pgzrun a.py")

main()