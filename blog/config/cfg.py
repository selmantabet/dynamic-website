from dotenv import load_dotenv
import os

cwd = os.getcwd()
env_path = os.path.join(cwd, "env", "vars.env")
print("cfg env path: ", env_path)
if (os.path.exists(env_path)):
    load_dotenv(dotenv_path=env_path)
    print("env vars initialized from config")
