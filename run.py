from blog import create_app, manager

manager = create_app()

if __name__ == '__main__':
    manager.run()