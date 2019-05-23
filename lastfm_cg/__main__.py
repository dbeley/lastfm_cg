"""
Create lastfm album collage for an user
"""
import logging
import time
import argparse
import configparser
import pylast
import requests
import os
import numpy as np
from PIL import Image
from io import BytesIO

logger = logging.getLogger()
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("numpy").setLevel(logging.WARNING)

temps_debut = time.time()

FORMAT = '%(levelname)s :: %(message)s'
TIMEFRAME_VALUES = ['7day',
                    '1month',
                    '3month',
                    '6month',
                    '12month',
                    'overall']

MAX_ROW_VALUE = 10


def lastfmconnect():
    # Lastfm config file parsing
    user_config_dir = os.path.expanduser("~/.config/lastfm_cg/")
    try:
        config = configparser.ConfigParser()
        config.read(user_config_dir + 'config.ini')
        API_KEY = config['lastfm']['API_KEY']
        API_SECRET = config['lastfm']['API_SECRET']
    except Exception as e:
        logger.error(("Error with the config file. Be sure to have a valid "
                      "~/.config/lastfm_cg/config.ini file. Error : %s"), e)
        if not os.path.exists(user_config_dir):
            logger.info(("Configuration folder not found. "
                         "Creating ~/.config/lastfm_cg/."))
            os.makedirs(user_config_dir)
        if not os.path.isfile(user_config_dir + "config.ini"):
            sample_config = ("[lastfm]\n"
                             "API_KEY=API_KEY_HERE\n"
                             "API_SECRET=API_SECRET_HERE\n"
                             )
            with open(user_config_dir + "config.ini", 'w') as f:
                f.write(sample_config)
            logger.info(("A sample configuration file has been created at "
                         "~/.config/lastfm_cg/config.ini. Go to "
                         "https://www.last.fm/api to create your own API keys "
                         "and put them in the configuration file."))
        exit()
    network = pylast.LastFMNetwork(api_key=API_KEY,
                                   api_secret=API_SECRET)
    return network


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def main():
    args = parse_args()
    network = lastfmconnect()
    if args.username:
        user = network.get_user(args.username)
    else:
        logger.error("Use the -u/--username flag to set an username.")
        exit()

    if args.timeframe not in TIMEFRAME_VALUES:
        logger.error("Incorrect value for timeframe. Accepted values : %s",
                     TIMEFRAME_VALUES)
    if args.rows > MAX_ROW_VALUE or not isinstance(args.rows, int):
        logger.error("Incorrect value for number of rows.\
                Max value : %s", MAX_ROW_VALUE)

    try:
        top_albums = user.get_top_albums(period=args.timeframe,
                                         limit=args.rows**2)
        if len(top_albums) != args.rows**2:
            logger.error("Not enough albums")
            exit()
        logger.debug("top_albums : %s", top_albums)
        list_covers = [album.item.get_cover_image() for album in top_albums]
        logger.debug("list_covers : %s", list_covers)

        list_responses = [requests.get(url).content for url in list_covers]
        imgs = [Image.open(BytesIO(i)) for i in list_responses]

        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

        list_comb = []
        for img in chunks(imgs, args.rows):
            list_arrays = [np.asarray(i.resize(min_shape)) for i in img]
            list_comb.append(np.hstack(list_arrays))

        list_comb_arrays = [np.asarray(i) for i in list_comb]
        imgs_comb = np.vstack(list_comb_arrays)
        imgs_comb = Image.fromarray(imgs_comb)

        export_filename = (f"{args.timeframe}_{args.username}_"
                           f"{int(time.time())}.png")
        imgs_comb.save(export_filename)
    except Exception as e:
        logger.error(e)
        exit()

    logger.debug("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Create lastfm album collage\
            for an user')
    parser.add_argument('--debug', help="Display debugging information",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG,
                        default=logging.INFO)
    parser.add_argument('--timeframe', '-t',
                        help="Timeframe (Accepted values : 7day, 1month,\
                              3month, 6month, 12month, overall.\
                              Default : 7day).",
                        type=str,
                        default="7day")
    parser.add_argument('--rows', '-r',
                        help="Number of rows\
                             (Maximum value : 10. Default : 5)",
                        type=int,
                        default=5)
    parser.add_argument('--username', '-u', help="Name of the user", type=str)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=FORMAT)
    return args


if __name__ == '__main__':
    main()
