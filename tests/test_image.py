import requests
from lastfm_cg import image_utils


def test_chunks():
    lst = range(10)
    lst_chunks = image_utils.chunks(lst, 2)
    for chunk in lst_chunks:
        assert len(chunk) == 2


def test_image(network_lastfm):
    url_cover = network_lastfm.get_album("XTC", "Go 2").get_cover_image()

    assert url_cover.startswith("https")
    assert url_cover.endswith(".png")

    cover = requests.get(url_cover).content

    list_cover = [cover] * 10

    image = image_utils.create_image(list_cover, 5)
    width, height = image.size
    assert width == 1500
    assert height == 600
