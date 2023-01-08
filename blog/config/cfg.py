from dotenv import load_dotenv
import os

cwd = os.getcwd()
base_env_path = os.path.join(cwd, "blog", "env", "base.env")
print("base env path: ", base_env_path)
if (os.path.exists(base_env_path)):
    load_dotenv(dotenv_path=base_env_path)
    print("base env vars initialized from config")

# Need a method to distinguish between dev and prod

SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppresses SQLAlchemy warnings
# Load the dev env vars anyway, for now
dev_env_path = os.path.join(cwd, "blog", "env", "dev.env")
print("dev env path: ", dev_env_path)
if (os.path.exists(dev_env_path)):
    load_dotenv(dotenv_path=dev_env_path)
    print("dev env vars initialized from config")

if os.environ["DB_MODE"] == "postgres":
    SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ["POSTGRESQL_USER"],
        dbpass=os.environ["POSTGRESQL_PASSWORD"],
        dbhost=os.environ["POSTGRESQL_ADDRESS"],
        dbname=os.environ["POSTGRESQL_DB_NAME"]
    )

else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(cwd, "blog", 'blog.db')

# EXAMPLE:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c123456:MySQLPassword@csmysql.cs.cf.ac.uk:3306/my_blog_db'
# WHERE:
# 'c123456' is your username (Student Number with leading 'c');
# 'MySQLPassword' is your MySQL password, NOT your University password! These two passwords SHOULD be different for security reasons. Use https://dbmanager.cs.cf.ac.uk/ to manage your passwords
# 'my_blog_db' is the name of your MySQL database
