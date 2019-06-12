from lastfm_cg import lastfm_utils


class EmulateTopList:
    def __init__(self, item):
        self.item = item


def test_user_lastfm(network_lastfm):
    user = network_lastfm.get_user("diyod")
    assert str(user) == "diyod"


def test_get_cover_from_album(network_lastfm):
    top_album = network_lastfm.get_user("diyod").get_top_albums(
        period="overall", limit=1
    )
    img = lastfm_utils.get_cover_for_album("01", top_album[0])
    assert type(img) is bytes


def test_get_list_covers(network_lastfm):
    list_covers = lastfm_utils.get_list_covers(
        network_lastfm.get_user("diyod"), 1, "overall"
    )
    assert len(list_covers) == 1


def test_album_none(network_lastfm):
    album = network_lastfm.get_album("Weezer", "Pinkerton")
    top_list = EmulateTopList(album)

    cover = lastfm_utils.get_cover_for_album(1, top_list)
    assert cover is None
