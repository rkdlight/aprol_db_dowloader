from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class Settings(BaseSettings):
    ODBC_DIVER:str
    ODBC_SERVER:str
    ODBC_PORT:int
    ODBC_USER:str
    ODBC_PASSWORD:str
    ODBC_PROJECT:str


    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def odbc_connection_string(self):
        return "".join([
            f"DRIVER={self.ODBC_DIVER};",
            f"SERVERLIST={self.ODBC_SERVER} {self.ODBC_PORT};",
            f"SYSTEM=aprolsys;",
            f"PROJECT={self.ODBC_PROJECT};",
            f"UseSsl=0;",
            f"UID={self.ODBC_USER};",
            f"PWD={self.ODBC_PASSWORD};",
        ])


settings = Settings()