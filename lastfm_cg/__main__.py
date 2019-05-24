"""
Create lastfm album collage for an user
"""
import logging
import time
import argparse
import configparser
import pylast
import requests
import requests_cache
import os
import numpy as np
from tqdm import tqdm
from PIL import Image
from io import BytesIO

logger = logging.getLogger()
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("numpy").setLevel(logging.WARNING)

temps_debut = time.time()

FORMAT = "%(levelname)s :: %(message)s"
TIMEFRAME_VALUES = ["7day", "1month", "3month", "6month", "12month", "overall"]


def lastfmconnect():
    # Lastfm config file parsing
    user_config_dir = os.path.expanduser("~/.config/lastfm_cg/")
    try:
        config = configparser.ConfigParser()
        config.read(user_config_dir + "config.ini")
        API_KEY = config["lastfm"]["API_KEY"]
        API_SECRET = config["lastfm"]["API_SECRET"]
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
                "API_KEY=API_KEY_HERE\n"
                "API_SECRET=API_SECRET_HERE\n"
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
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    return network


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def main():
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
        user = network.get_user(args.username)
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
        logger.error(
            "Incorrect value %s for number of rows.",
            args.columns,
            MAX_ROW_VALUE,
        )
        exit()
    if not isinstance(args.columns, int):
        logger.error(
            "Incorrect value %s for number of columns.",
            args.columns,
            MAX_ROW_VALUE,
        )
        exit()
    if args.columns * args.rows > 1000:
        logger.error(
            "Can't extract more than 1000 albums. Choose smaller number of rows/columns."
        )
        exit()

    try:
        logger.info("Retrieving top albums.")
        top_albums = user.get_top_albums(
            period=args.timeframe, limit=args.rows * args.columns
        )
        if len(top_albums) != args.rows * args.columns:
            logger.error(
                "Not enough albums. Choose a lower rows/columns value or another timeframe."
            )
            exit()
        logger.debug("len top_albums : %s", len(top_albums))
        list_covers = []
        for index, album in enumerate(tqdm(top_albums, dynamic_ncols=True), 1):
            try:
                logger.debug(
                    "Retrieving cover for album %s - %s", index, album.item
                )
                list_covers.append(album.item.get_cover_image())
            except Exception as e:
                logger.warning("%s : %s", album.item, e)
        list_covers = [x for x in list_covers if x is not None]
        logger.debug("len list_covers : %s", len(list_covers))

        logger.info("Downloading cover images.")
        list_responses = [
            requests.get(url).content
            for url in tqdm(list_covers, dynamic_ncols=True)
        ]
        imgs = [Image.open(BytesIO(i)) for i in list_responses]

        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

        logger.info("Creating image.")
        list_comb = []
        for img in chunks(imgs, args.columns):
            list_arrays = [np.asarray(i.resize(min_shape)) for i in img]
            logger.debug("len list_arrays : %s", list_arrays)
            i = 0
            while len(list_arrays) < args.columns:
                i += 1
                logger.debug(
                    "Missing album cover. Creating empty square %s.", i
                )
                list_arrays.append(
                    np.asarray(
                        np.zeros(
                            (min_shape[0], min_shape[1], 4), dtype=np.uint8
                        )
                    )
                )
            list_comb.append(np.hstack(list_arrays))

        list_comb_arrays = [np.asarray(i) for i in list_comb]
        imgs_comb = np.vstack(list_comb_arrays)
        imgs_comb = Image.fromarray(imgs_comb)

        export_filename = (
            f"{args.timeframe}_{args.username}_" f"{int(time.time())}.png"
        )
        imgs_comb.save(export_filename)
    except Exception as e:
        logger.error(e)
        exit()

    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create lastfm album collage\
            for an user"
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
        help="Number of rows (Maximum value : 31. Default : 5).",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--columns",
        "-c",
        help="Number of columns (Maximum value : 31. Default : number of rows).",
        type=int,
    )
    parser.add_argument("--username", "-u", help="Name of the user", type=str)
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
