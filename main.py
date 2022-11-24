import os
from webapp import create_app

env = os.environ.get('WEBAPP_ENV', 'dev')
print(env, 'env')

app = create_app(f'config.{env.capitalize()}Config')

if __name__ == '__main__':
    app.run()
