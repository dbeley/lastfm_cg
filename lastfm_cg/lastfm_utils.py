import requests
from tqdm import tqdm
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)


def get_cover_for_album(index, album):
    # returns an img object for an album or None
    nb_tries = 0
    while True:
        try:
            nb_tries += 1
            url = album.item.get_cover_image()
            break
        except Exception as e:
            logger.warning(
                "Error retrieving cover url for %s - %s : %s. " "Retrying.",
                index,
                album.item,
                e,
            )
            if nb_tries > 4:
                logger.warning(
                    "Couldn't retrieve cover url for %s - %s after "
                    "4 tries.",
                    index,
                    album.item,
                )
                url = None
                break
    if url:
        logger.debug("URL : %s", url)
        if url.endswith(".png") or url.endswith(".jpg"):
            img = requests.get(url).content
            if img:
                try:
                    Image.open(BytesIO(img)).seek(1)
                except EOFError:
                    return img
                else:
                    # image is a gif
                    logger.warning("Image is a gif. Skipping")
            else:
                # link returned by get_cover_image() doesn't work
                logger.warning("No image returned by url %s", url)
        else:
            # url doesn't host a png or jpg image
            logger.warning("Wrong filetype for %s", url)
    else:
        # no url returned by get_cover_image()
        logger.warning("No cover image found for %s - %s", index, album.item)
    return None


def extract_covers_from_top_albums(top_albums):
    # extract all correct img from a top_albums list
    list_covers = []
    for index, album in enumerate(tqdm(top_albums, dynamic_ncols=True), 1):
        logger.debug("Retrieving cover for album %s - %s.", index, album.item)
        img = get_cover_for_album(index, album)
        if img:
            list_covers.append(img)
    return list_covers


def get_list_covers(user, nb_covers, timeframe):
    # extract the top available covers for the specified timeframe and user
    nb_failed = 0
    nb_failed_global = 0
    list_covers = []
    # while at least one cover extraction fails
    while True:
        # keep track of all the failed ones, in case of several iterations
        nb_failed_global += nb_failed
        limit = nb_covers + nb_failed_global
        if nb_failed > 0:
            logger.info(
                "Some covers weren't properly extracted. "
                "Adding %s albums to the grid.",
                nb_failed,
            )
        logger.info(
            "Retrieving top %s albums covers for %s.", limit, str(user)
        )
        if limit > 1000:
            logger.error(
                "Can't extract more than 1000 albums. "
                "Choose smaller number of rows/columns."
            )
            exit()
        top_albums = user.get_top_albums(period=timeframe, limit=limit)
        if len(top_albums) != limit:
            logger.error(
                "Not enough albums played in the selected timeframe. "
                "Choose a lower rows/columns value or another timeframe."
            )
            exit()
        top_albums = top_albums[-nb_failed:]
        logger.debug("len(top_albums) : %s", len(top_albums))
        nb_failed = 0
        list_covers_partial = extract_covers_from_top_albums(top_albums)
        nb_failed = len(top_albums) - len(list_covers_partial)
        list_covers += list_covers_partial
        if nb_failed == 0:
            break
    return list_covers
