#Этот файл нужен для скрывания токена бота, который обращается к файлу .env, в нем указан наш токен от бота
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, ValidationError
class Settings(BaseSettings):
    # Желательно вместо str использовать SecretStr 
    # для конфиденциальных данных, например, токена бота
    bot_token: SecretStr
    
    # Начиная со второй версии pydantic, настройки класса настроек задаются
    # через model_config
    # В данном случае будет использоваться файла .env, который будет прочитан
    # с кодировкой UTF-8
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

# При импорте файла сразу создастся 
# и провалидируется объект конфига, 
# который можно далее импортировать из разных мест
print("Значение BOT_TOKEN:", os.getenv('BOT_TOKEN'))
config = Settings()