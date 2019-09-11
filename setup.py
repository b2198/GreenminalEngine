import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GreenminalEngine",
    version="0.0.1",
    author="Breno Alencar (b2198)",
    author_email="onerb98@hotmail.com",
    description="A terminal-based small game engine for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/b2198/GreenminalEngine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)