import requests
from lastfm_cg import image_utils


def test_chunks():
    lst = range(10)
    lst_chunks = image_utils.chunks(lst, 2)
    for chunk in lst_chunks:
        if not len(chunk) == 2:
            raise AssertionError()


def test_image(network_lastfm):
    url_cover = network_lastfm.get_album("XTC", "Go 2").get_cover_image()

    if not url_cover.startswith("https"):
        raise AssertionError()
    if not (url_cover.endswith(".png") or url_cover.endswith(".jpg")):
        raise AssertionError()

    cover = requests.get(url_cover).content

    list_cover = [cover] * 10

    image = image_utils.create_image(list_cover, 5)
    width, height = image.size
    if not width == 1500:
        raise AssertionError()
    if not height == 600:
        raise AssertionError()


def test_top100_image(network_lastfm):
    url_cover = network_lastfm.get_album("XTC", "Mummer").get_cover_image()

    if not url_cover.startswith("https"):
        raise AssertionError()
    if not (url_cover.endswith(".png") or url_cover.endswith(".jpg")):
        raise AssertionError()

    cover = requests.get(url_cover).content

    list_cover_top100 = [cover] * 100

    image = image_utils.create_top100_image(list_cover_top100)
    width, height = image.size

    if not width == 1500:
        raise AssertionError()
    if not height == 1450:
        raise AssertionError()
