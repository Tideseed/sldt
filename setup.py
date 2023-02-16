from setuptools import setup, find_packages

setup(
    name="sldt",
    version="0.1",
    author="Robokami",
    description="SLDT Client",
    packages=find_packages(),
    install_requires=["requests", "sseclient-py", "pydantic"],
    python_requires=">=3.10",
)
