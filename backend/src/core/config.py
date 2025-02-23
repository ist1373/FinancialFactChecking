"""
Config
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    
    DATABASE_URL: str = "mysql+pymysql://admin:addmin_pass@localhost:3306/fact_checking_db"

    LLM_HOST_URL: str = "http://development-auto-deploy.triton-vllm-backend-55317507-development.svc.cluster.local"
    LLM_HOST_ENDPOINT: str = '/v2/models/vllm_model/generate'

    LLM_FACT_CHECKER_URL:str = "http://development-auto-deploy.fact-checking-43999443-development.svc.cluster.local"
    LLM_CLAIM_EXTRACTION_ENDPOINT:str = "llm-claim-extraction"
    LLM_CLAIM_VERIFICATION_ENDPOINT:str = "llm-claim-verification"

    class Config:
        env_file = ".env"

settings = Settings()

# fact-checker-sql-container