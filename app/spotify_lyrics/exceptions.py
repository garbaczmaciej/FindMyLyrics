class SpotifyError(Exception):
    pass


class SpotifyRequestError(SpotifyError):
    pass


class SpotifyIdError(SpotifyError):
    pass


class SpotifyTrackNotFound(SpotifyError):
    pass


class ServerScrapingError(Exception):
    pass


class LyricsNotFound(Exception):
    pass
