"""
Create lastfm album collage for an user
"""
import logging
import time
import argparse
import configparser
import pylast
import requests_cache
import os
from lastfm_cg import image_utils
from lastfm_cg import lastfm_utils

logger = logging.getLogger()
logging.getLogger("requests").setLevel(logging.WARNING)

temps_debut = time.time()

FORMAT = "%(levelname)s :: %(message)s"
TIMEFRAME_VALUES = ["7day", "1month", "3month", "6month", "12month", "overall"]


def lastfmconnect():
    # Lastfm config file parsing
    user_config_dir = os.path.expanduser("~/.config/lastfm_cg/")
    try:
        config = configparser.ConfigParser()
        config.read(user_config_dir + "config.ini")
        api_key = config["lastfm"]["api_key"]
        api_secret = config["lastfm"]["api_secret"]
    except Exception as e:
        logger.error(
            (
                "Error with the config file. Be sure to have a valid "
                "~/.config/lastfm_cg/config.ini file. Error : %s"
            ),
            e,
        )
        if not os.path.exists(user_config_dir):
            logger.info(
                (
                    "Configuration folder not found. "
                    "Creating ~/.config/lastfm_cg/."
                )
            )
            os.makedirs(user_config_dir)
        if not os.path.isfile(user_config_dir + "config.ini"):
            sample_config = (
                "[lastfm]\n"
                "api_key=api_key_here\n"
                "api_secret=api_secret_here\n"
            )
            with open(user_config_dir + "config.ini", "w") as f:
                f.write(sample_config)
            logger.info(
                (
                    "A sample configuration file has been created at "
                    "~/.config/lastfm_cg/config.ini. Go to "
                    "https://www.last.fm/api to create your own API keys "
                    "and put them in the configuration file."
                )
            )
        exit()
    network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    return network


def main():
    # argument parsing
    args = parse_args()
    network = lastfmconnect()

    if not args.columns:
        args.columns = args.rows

    # cache for python-requests
    if not args.disable_cache:
        cache_folder = os.path.expanduser("~/.local/share/lastfm_cg/")
        if not os.path.exists(cache_folder):
            logger.info("Cache folder not found. Creating %s", cache_folder)
            os.makedirs(cache_folder)
            if not os.path.isfile(cache_folder + "lastfm_cg_cache.sqlite"):
                original_folder = os.getcwd()
                os.chdir(cache_folder)
                requests_cache.install_cache("lastfm_cg_cache")
                os.chdir(original_folder)
    requests_cache.configure(
        os.path.expanduser(cache_folder + "lastfm_cg_cache")
    )

    if args.username:
        users = [x.strip() for x in args.username.split(",")]
    else:
        logger.error("Use the -u/--username flag to set an username.")
        exit()

    if args.timeframe not in TIMEFRAME_VALUES:
        logger.error(
            "Incorrect value %s for timeframe. Accepted values : %s",
            args.columns,
            TIMEFRAME_VALUES,
        )
        exit()
    if not isinstance(args.rows, int):
        logger.error("Incorrect value %s for number of rows.", args.columns)
        exit()
    if not isinstance(args.columns, int):
        logger.error("Incorrect value %s for number of columns.", args.columns)
        exit()

    for username in users:
        user = network.get_user(username)

        nb_covers = args.rows * args.columns
        list_covers = lastfm_utils.get_list_covers(
            user=user, nb_covers=nb_covers, timeframe=args.timeframe
        )
        img = image_utils.create_image(
            list_covers=list_covers, nb_columns=args.columns
        )

        # export image
        export_filename = f"{args.timeframe}_{username}_{args.columns*args.rows:004}_{int(time.time())}.png"
        img.save(export_filename)

    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create lastfm album collage\
            for one or several lastfm users."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "--timeframe",
        "-t",
        help="Timeframe (Accepted values : 7day, 1month,\
                              3month, 6month, 12month, overall.\
                              Default : 7day).",
        type=str,
        default="7day",
    )
    parser.add_argument(
        "--rows",
        "-r",
        help="Number of rows (Default : 5).",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--columns",
        "-c",
        help="Number of columns (Default : number of rows).",
        type=int,
    )
    parser.add_argument(
        "--username",
        "-u",
        help="Usernames to extract, separated by comma.",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--disable_cache",
        help="Disable the cache",
        dest="disable_cache",
        action="store_true",
    )
    parser.set_defaults(disable_cache=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=FORMAT)
    return args


if __name__ == "__main__":
    main()
