import setuptools

with open("README.md", "r") as fh:
    readme = fh.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name="git-history-tools",
    version="0.0.1",
    author="Orlando Tomás",
    author_email="orlando.tomas@hotmail.com",
    description="Group GIT commits by user and show changes in a compact mode",
    url="https://github.com/orltom/git-history-tools",
    long_description=readme,
    license=license,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    scripts=['cli.py'],
    python_requires='>=3.6',
)
