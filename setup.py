import setuptools
import lastfm_cg

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lastfm_cg",
    version=lastfm_cg.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="Generate covers collage from albums listened by a lastfm user.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/lastfm_cg",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["lastfm_cg=lastfm_cg.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "pylast",
        "numpy",
        "pillow",
        "requests",
        "requests-cache",
        "tqdm",
    ],
)
