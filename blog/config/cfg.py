from dotenv import load_dotenv
import os

# Based on a self-developed config script used in Snoonu Qatar's backend FalconFlex system.

cwd = os.getcwd()
base_env_path = os.path.join(cwd, "blog", "env", "base.env")
print("base env path: ", base_env_path)
if (os.path.exists(base_env_path)):
    load_dotenv(dotenv_path=base_env_path)
    print("base env vars initialized from config")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppresses SQLAlchemy warnings

# Load the dev env vars anyway, for now
dev_env_path = os.path.join(cwd, "blog", "env", "dev.env")
print("dev env path: ", dev_env_path)
if (os.path.exists(dev_env_path)):
    load_dotenv(dotenv_path=dev_env_path)
    print("dev env vars initialized from config")

if os.environ.get("ENV_TYPE") == "OPENSHIFT":
    print("OpenShift deployment detected.")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ["MYSQL_USER"],
        dbpass=os.environ["MYSQL_PASSWORD"],
        dbhost=os.environ["MYSQL_ADDRESS"],
        dbname=os.environ["MYSQL_DB_NAME"]
    )
else:
    prod_env_path = os.path.join(cwd, "blog", "env", "prod.env")
    print("prod env path: ", prod_env_path)
    if (os.path.exists(prod_env_path)):
        load_dotenv(dotenv_path=prod_env_path)
        print("prod env vars initialized from config")

    if os.environ.get("DB_MODE") == "postgres":
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=os.environ["POSTGRESQL_USER"],
            dbpass=os.environ["POSTGRESQL_PASSWORD"],
            dbhost=os.environ["POSTGRESQL_ADDRESS"],
            dbname=os.environ["POSTGRESQL_DB_NAME"]
        )
    elif os.environ.get("DB_MODE") == "mysql":
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=os.environ["MYSQL_USER"],
            dbpass=os.environ["MYSQL_PASSWORD"],
            dbhost=os.environ["MYSQL_ADDRESS"],
            dbname=os.environ["MYSQL_DB_NAME"]
        )
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
            os.path.join(cwd, "blog", 'blog.db')
