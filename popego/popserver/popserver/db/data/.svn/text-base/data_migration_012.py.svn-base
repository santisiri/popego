__docformat__ = "restructuredtext"

migration = [
    ("""\
         INSERT INTO globalconfig VALUES
             ('popcard.default.images.artist', '/images/widget/default/artist.png');
         INSERT INTO globalconfig VALUES
             ('popcard.default.images.artist.small', '/images/widget/default/artist_small.png');
      """,
    """\
         DELETE FROM globalconfig WHERE 
             property = 'popcard.default.images.artist';
         DELETE FROM globalconfig WHERE 
             property = 'popcard.default.images.artist.small';
    """),
]
