from lastfm_cg import lastfm_utils


class EmulateTopListItem:
    def __init__(self, item):
        self.item = item


def test_user_lastfm(network_lastfm):
    user = network_lastfm.get_user("diyod")
    if not str(user) == "diyod":
        raise AssertionError()


def test_get_cover_from_album(network_lastfm):
    top_album = network_lastfm.get_user("diyod").get_top_albums(
        period="overall", limit=1
    )
    img = lastfm_utils.get_cover_for_album("01", top_album[0])
    if not isinstance(img, bytes):
        raise AssertionError()


def test_get_list_covers(network_lastfm):
    list_covers = lastfm_utils.get_list_covers(
        network_lastfm.get_user("diyod"), 1, "overall"
    )
    if not len(list_covers) == 1:
        raise AssertionError()


def test_album_gif(network_lastfm):
    album = network_lastfm.get_album("Weezer", "Pinkerton")
    top_list = EmulateTopListItem(album)

    cover = lastfm_utils.get_cover_for_album(1, top_list)
    if cover is not None:
        raise AssertionError()


def test_album_unavailable(network_lastfm):
    album = network_lastfm.get_album("King Crimson", "Red")
    top_list = EmulateTopListItem(album)

    cover = lastfm_utils.get_cover_for_album(1, top_list)
    if cover is not None:
        raise AssertionError()
