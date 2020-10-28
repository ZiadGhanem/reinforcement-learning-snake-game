from app import App

GRID_SIZE = 16
WINDOW_SIZE = 640

def main():
    theApp = App(WINDOW_SIZE, GRID_SIZE)
    theApp.on_execute()

if __name__ == "__main__" :
    main()
