import setuptools
import bot_lastfm_cg

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bot_lastfm_cg",
    version=bot_lastfm_cg.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="Post new lastfm_cg collages from a directory to twitter or mastodon.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/lastfm_cg/bot_lastfm_cg",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["bot_lastfm_cg=bot_lastfm_cg.__main__:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["tweepy", "pillow", "Mastodon.py"],
)
