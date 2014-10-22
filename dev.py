import os

if __name__ == "__main__":
    os.environ['CONFIG_ENV'] = 'Development'

    from app import create_app
    create_app(os.environ['CONFIG_ENV']).run()
