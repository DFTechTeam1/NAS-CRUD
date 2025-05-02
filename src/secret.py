import os
from dotenv import load_dotenv

env_file = os.getenv("ENV_FILE", "env/.env.development")

if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    raise FileNotFoundError(f"Environment file {env_file} not found.")
