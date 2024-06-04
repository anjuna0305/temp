from dotenv import load_dotenv, dotenv_values

load_dotenv()
env_values = dotenv_values()

print(env_values.get("SQLALCHEMY_DATABASE_URL"))