import logging
import configparser
import datetime
import argparse
import tweepy
from PIL import Image
from pathlib import Path
from mastodon import Mastodon

logger = logging.getLogger()
logging.getLogger("requests_oauthlib").setLevel(logging.CRITICAL)
config = configparser.ConfigParser()
config.read("config.ini")
begin_time = datetime.datetime.now()
SUPPORTED_SOCIAL_MEDIA = ["twitter", "mastodon"]
TIMEFRAME_VALUES = ["7day", "1month", "3month", "6month", "12month", "overall"]


def twitterconnect():
    consumer_key = config["twitter"]["consumer_key"]
    secret_key = config["twitter"]["secret_key"]
    access_token = config["twitter"]["access_token"]
    access_token_secret = config["twitter"]["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def tweet_image(api, filename, title, social_media):
    if social_media == "twitter":
        pic = api.media_upload(str(filename))
        api.update_status(status=title, media_ids=[pic.media_id_string])
    elif social_media == "mastodon":
        id_media = api.media_post(str(filename), "image/png")
        api.status_post(title, media_ids=[id_media])


def mastodonconnect():
    if not Path("mastodon_clientcred.secret").is_file():
        Mastodon.create_app(
            "mastodon_bot_lastfm_cg",
            api_base_url=config["mastodon"]["api_base_url"],
            to_file="mastodon_clientcred.secret",
        )

    if not Path("mastodon_usercred.secret").is_file():
        mastodon = Mastodon(
            client_id="mastodon_clientcred.secret",
            api_base_url=config["mastodon"]["api_base_url"],
        )
        mastodon.log_in(
            config["mastodon"]["login_email"],
            config["mastodon"]["password"],
            to_file="mastodon_usercred.secret",
        )

    mastodon = Mastodon(
        access_token="mastodon_usercred.secret",
        api_base_url=config["mastodon"]["api_base_url"],
    )
    return mastodon


def main():
    args = parse_args()
    social_media = args.social_media.lower()
    if args.no_upload:
        logger.debug("No upload mode activated.")
    else:
        if social_media not in SUPPORTED_SOCIAL_MEDIA:
            logger.error("%s not supported. Exiting.", social_media)
            exit()
        elif social_media == "twitter":
            api = twitterconnect()
            done_filename = "DONE_twitter.txt"
        elif social_media == "mastodon":
            api = mastodonconnect()
            done_filename = "DONE_mastodon.txt"

    if args.timeframe == "all":
        list_active_timeframes = TIMEFRAME_VALUES
    elif args.timeframe not in TIMEFRAME_VALUES:
        logger.error(
            "Wrong value for timeframe. Choose another value among %s.",
            TIMEFRAME_VALUES,
        )
        exit()
    else:
        list_active_timeframes = [args.timeframe]
    logger.debug(f"Posting images from timeframes : {list_active_timeframes}.")

    if args.directory:
        logger.debug("Posting images from directory %s.", args.directory)
    else:
        args.directory = Path()
        logger.debug("Posting images from directory %s.", args.directory)

    image_list = Path(args.directory).glob("*.png")

    if not args.no_upload and Path(done_filename).is_file():
        with open(done_filename, "r") as f:
            done_list = [x.strip() for x in f.readlines()]
    else:
        done_list = []
    logger.debug(f"Images already posted : {done_list}.")

    with open(args.template_file, "r") as myfile:
        tweet_template = myfile.read()

    for image in sorted(image_list):
        logger.debug("Image %s.", image.name)
        try:
            # won't work well if the lastfm username has an undersore in it
            image_name = image.name.split("_")
            timeframe = image_name[0]
            current_timeframe = timeframe
            username = image_name[1]
            if timeframe == "7day":
                start = begin_time - datetime.timedelta(weeks=1)
                timeframe = f"for the week of {start.strftime('%B %d %Y')}"
                logger.debug("timeframe : 7day")
            elif timeframe == "1month":
                start = begin_time - datetime.timedelta(weeks=1)
                timeframe = f"for {start.strftime('%B %Y')}"
                logger.debug("timeframe : 1month")
            elif timeframe == "3month":
                timeframe = "for the last 3 months"
                logger.debug("timeframe : 3month")
            elif timeframe == "6month":
                timeframe = "for the last 6 months"
                logger.debug("timeframe : 6month")
            elif timeframe == "12month":
                start = begin_time - datetime.timedelta(weeks=1)
                timeframe = f"for the year {start.strftime('%Y')}"
                logger.debug("timeframe : 12month")
            elif timeframe == "overall":
                timeframe = "ever"
                logger.debug("timeframe : overall")
            title = eval(tweet_template)

            if (
                str(image.absolute()) not in done_list
                and current_timeframe in list_active_timeframes
            ):
                logger.info("Image %s not already posted.", image.name)
                if args.no_upload:
                    logger.info(
                        (
                            "No posting mode activated.\n"
                            "File : %s\n"
                            "message : %s\n"
                        ),
                        image.name,
                        title,
                    )
                else:
                    try:
                        logger.info(
                            "Uploading %s with message %s.", image.name, title
                        )
                        tweet_image(api, image, title, social_media)
                        if not args.no_upload:
                            with open(done_filename, "a") as f:
                                f.write(f"{str(image.absolute())}\n")
                    except Exception as e:
                        logger.error("Error uploading image : %s.", e)
                        # can't upload original image, resizing until if fits
                        size = 1024, 1024
                        while True:
                            try:
                                logger.info(
                                    "Image too big. Trying resize at size %s.",
                                    size[0],
                                )
                                im = Image.open(image)
                                im.thumbnail(size)
                                im.save("temp.png", "PNG")
                                converted_image = Path("temp.png")
                                logger.info("Retrying upload.")
                                tweet_image(
                                    api, converted_image, title, social_media
                                )
                                if not args.no_upload:
                                    with open(done_filename, "a") as f:
                                        f.write(f"{str(image.absolute())}\n")
                                logger.info(
                                    "Upload of %s successful.", image.name
                                )
                                break
                            except Exception as e:
                                logger.error("Error uploading image : %s.", e)
                                size = int(size[0] / 1.25), int(size[1] / 1.25)
            else:
                logger.info(
                    "Image %s already posted or timeframe invalid.", image.name
                )
        except Exception as e:
            logger.error(e)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bot posting images from lastfm_cg to twitter or mastodon."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory containing the images to post (Default : current directory).",
        type=str,
    )
    parser.add_argument(
        "--no_upload",
        help="Disable the upload.",
        dest="no_upload",
        action="store_true",
    )
    parser.add_argument(
        "--social_media",
        "-s",
        help="Social media where the image will be posted (twitter or mastodon. Default : twitter).",
        default="twitter",
        type=str,
    )
    parser.add_argument(
        "--timeframe",
        "-t",
        help="Only post pictures for a specific timeframe (Available choices : 7day, 1month, 3month, 6month, 12month, overall, all).",
        default="all",
        type=str,
    )
    parser.add_argument(
        "--template_file",
        help="Text file containing the template for the tweet (Default : tweet_template.txt).",
        default="tweet_template.txt",
        type=str,
    )
    parser.set_defaults(no_upload=False)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
