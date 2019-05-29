import logging
import configparser
import datetime
import argparse
import tweepy
from PIL import Image
from pathlib import Path

logger = logging.getLogger()
logging.getLogger("requests_oauthlib").setLevel(logging.CRITICAL)
config = configparser.ConfigParser()
config.read("config.ini")
begin_time = datetime.datetime.now()


def twitterconnect():
    ConsumerKey = config["twitter"]["ConsumerKey"]
    SecretKey = config["twitter"]["SecretKey"]
    AccessToken = config["twitter"]["AccessToken"]
    AccessTokenSecret = config["twitter"]["AccessTokenSecret"]

    auth = tweepy.OAuthHandler(ConsumerKey, SecretKey)
    auth.set_access_token(AccessToken, AccessTokenSecret)
    return tweepy.API(auth)


def tweet_image(api, filename, title):
    pic = api.media_upload(str(filename))
    api.update_status(status=title, media_ids=[pic.media_id_string])


def main():
    args = parse_args()
    if args.no_upload_twitter:
        logger.debug("No upload to twitter.")
    else:
        logger.debug("Upload to twitter.")
        api = twitterconnect()

    if args.directory:
        logger.debug("Using directory %s", args.directory)
    else:
        args.directory = Path()
        logger.debug("Using directory %s", args.directory)

    image_list = Path(args.directory).glob("*.png")

    done_filename = "DONE.txt"
    if Path(done_filename).is_file():
        with open(done_filename, "r") as f:
            done_list = [x.strip() for x in f.readlines()]
    else:
        done_list = []
    logger.info(done_list)

    for image in sorted(image_list):
        logger.debug("Image %s", image.name)
        try:
            # won't work well if the lastfm username has an undersore in it
            image_name = image.name.split("_")
            timeframe = image_name[0]
            if timeframe == "7day":
                # dt = datetime.datetime.strptime(begin_time, "%d/%b/%Y")
                start = begin_time - datetime.timedelta(
                    days=begin_time.weekday()
                )
                time = start + datetime.timedelta(days=6)
                # title = f"My most listened albums on #lastfm for week {begin_time.strftime('%U')} of {begin_time.strftime('%Y')}."
                title = (
                    f"My most listened albums on #lastfm for the week of {time.strftime('%B %d %Y')}\n"
                    f"Made with https://github.com/dbeley/lastfm_cg"
                )
                logger.debug("timeframe : 7day")
            elif timeframe == "1month":
                title = (
                    f"My most listened albums on #lastfm for {begin_time.strftime('%B %Y')}.\n"
                    f"Made with https://github.com/dbeley/lastfm_cg"
                )
                logger.debug("timeframe : 1month")
            elif timeframe == "3month":
                title = (
                    f"My most listened albums on #lastfm for the last 3 months.\n"
                    f"Made with https://github.com/dbeley/lastfm_cg"
                )
                logger.debug("timeframe : 3month")
            elif timeframe == "6month":
                title = (
                    f"My most listened albums on #lastfm for the last 6 months.\n"
                    f"Made with https://github.com/dbeley/lastfm_cg"
                )
                logger.debug("timeframe : 6month")
            elif timeframe == "12month":
                title = (
                    f"My most listened albums on #lastfm for the last 12 months.\n"
                    f"Made with https://github.com/dbeley/lastfm_cg"
                )
                logger.debug("timeframe : 12month")
            elif timeframe == "overall":
                title = (
                    f"My most listened albums on #lastfm ever.\n"
                    f"Made with https://github.com/dbeley/lastfm_cg"
                )
                logger.debug("timeframe : overall")

            if str(image.absolute()) not in done_list:
                # uploading to twitter:
                logger.info("Image %s not already posted.", image.name)
                if args.no_upload_twitter:
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
                            "Uploading %s with message %s", image.name, title
                        )
                        tweet_image(api, image, title)
                        with open(done_filename, "a") as f:
                            f.write(f"{str(image.absolute())}\n")
                    except Exception as e:
                        logger.error("Error uploading image : %s", e)
                        # can't upload original image, resizing until if fits
                        size = 1024, 1024
                        while True:
                            try:
                                logger.info(
                                    "Image too big. Trying resize at size %s",
                                    size[0],
                                )
                                im = Image.open(image)
                                im.thumbnail(size)
                                im.save("temp.png", "PNG")
                                converted_image = Path("temp.png")
                                logger.info("Retrying upload.")
                                tweet_image(api, converted_image, title)
                                with open(done_filename, "a") as f:
                                    f.write(f"{str(image.absolute())}\n")
                                logger.info(
                                    "Upload of %s successful.", image.name
                                )
                                break
                            except Exception as e:
                                logger.error("Error uploading image : %s", e)
                                size = int(size[0] / 1.25), int(size[1] / 1.25)
            else:
                logger.info("Image %s already posted.", image.name)
        except Exception as e:
            logger.error(e)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Twitter bot posting images from lastfm_cg"
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
        "-d",
        "--directory",
        help="Directory containing the images to post. Default : current directory.",
        type=str,
    )
    parser.add_argument(
        "--no_upload_twitter",
        help="Disable the twitter upload. Use it for debugging",
        dest="no_upload_twitter",
        action="store_true",
    )
    parser.set_defaults(no_upload_twitter=False)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
