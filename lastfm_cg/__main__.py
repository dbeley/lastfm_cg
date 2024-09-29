"""
Create lastfm album collage for an user
"""

import logging
import time
import argparse
import configparser
import pylast
import os
from lastfm_cg import image_utils
from lastfm_cg import lastfm_utils

logger = logging.getLogger()
logging.getLogger("requests").setLevel(logging.WARNING)

temps_debut = time.time()

FORMAT = "%(levelname)s :: %(message)s"
TIMEFRAME_VALUES = ["7day", "1month", "3month", "6month", "12month", "overall"]


def lastfmconnect(api_key=None, api_secret=None):
    if api_key and api_secret:
        network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
        return network
    else:
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
                    "[lastfm]\n" "api_key=api_key_here\n" "api_secret=api_secret_here\n"
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


def get_lastfm_collage(user, timeframe, rows, columns, top100):
    if top100:
        list_covers = lastfm_utils.get_list_covers(user, 100, timeframe)
        image = image_utils.create_top100_image(list_covers)
    else:
        list_covers = lastfm_utils.get_list_covers(user, rows * columns, timeframe)
        image = image_utils.create_image(list_covers, columns)
    return image


def main():
    # argument parsing
    args = parse_args()

    if args.API_KEY and args.API_SECRET:
        network = lastfmconnect(api_key=args.API_KEY, api_secret=args.API_SECRET)
    else:
        network = lastfmconnect()

    if not args.columns:
        args.columns = args.rows

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

    for username in users:
        user = network.get_user(username)

        nb_covers = args.rows * args.columns if not args.top100 else 100

        img = get_lastfm_collage(
            user, args.timeframe, args.rows, args.columns, args.top100
        )

        # export image
        if args.output_filename:
            export_filename = args.output_filename
        elif args.top100:
            export_filename = (
                f"{args.timeframe}_{username}_top100_{int(time.time())}.png"
            )
        else:
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
        "--top100",
        help="Create a top 100 image. Will override columns/rows.",
        dest="top100",
        action="store_true",
    )
    parser.add_argument("--API_KEY", help="Lastfm API key (optional)")
    parser.add_argument("--API_SECRET", help="Lastfm API secret (optional)")
    parser.add_argument(
        "--output_filename", help="Output filename (optional, example: output.png)"
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=FORMAT)
    return args


if __name__ == "__main__":
    main()
