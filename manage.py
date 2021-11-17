from exts import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps.cms import models
from run import create_app

app = create_app('develop')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
