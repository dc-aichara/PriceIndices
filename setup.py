import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
setuptools.setup(
    name="PriceIndices",
    packages=["PriceIndices"],
    version="1.3.0",
    license="MIT",
    description="A python package to get historical market data of "
                "cryptocurrencies, and calculate & plot "
                "different price technical indicators.",
    author="Dayal Chand Aichara",
    author_email="dc.aichara@gmail.com",
    url="https://github.com/dc-aichara/Price-Indices",
    download_url="https://github.com/dc-aichara/PriceIndices/archive/v1.3.0.tar.gz",
    keywords=[
        "Volatility",
        "blockchain",
        "cryptocurrency",
        "Price",
        "trading",
        "CoinMarketCap",
        "Indices",
        "Indicators",
    ],
    install_requires=["requests", "pandas", "numpy", "matplotlib"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
