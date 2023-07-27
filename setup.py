from setuptools import setup

setup(
    name="vintt4",
    version="1.1.0",

    python_requires=">=3.9",
    install_requires=[
        "psutil",
        "loguru",
        "fastapi",
        "pyyaml",
        "pydantic",
        "uvicorn"
    ]
)