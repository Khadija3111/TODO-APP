from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.0",
        "sqlmodel>=0.0.22",
        "uvicorn[standard]>=0.32.0",
        "passlib[bcrypt]>=1.7.4",
        "bcrypt>=4.0.1",
        "python-jose[cryptography]>=3.3.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.7.0",
        "aiosqlite>=0.20.0",
        "cryptography>=43.0.1",
        "typing-extensions>=4.8.0",
        "python-multipart>=0.0.12",
        "openai>=1.52.2",
        "cohere>=5.11.0",
    ],
    python_requires=">=3.13",
)