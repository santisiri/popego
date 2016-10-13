__docformat__ = "restructuredtext"

migration = [
    ("""\
         INSERT INTO globalconfig VALUES
             ('popcard.media.groupsPageSize', '8');
         INSERT INTO globalconfig VALUES
             ('popcard.media.picturesPageSize', '15');
         INSERT INTO globalconfig VALUES
             ('popcard.media.videosPageSize', '8');
         INSERT INTO globalconfig VALUES
             ('popcard.media.bookmarksPageSize', '5');
         INSERT INTO globalconfig VALUES
             ('popcard.media.ranksPageSize', '5');
      """,
    """\
         DELETE FROM globalconfig WHERE 
             property = 'popcard.media.groupsPageSize';
         DELETE FROM globalconfig WHERE 
             property = 'popcard.media.picturesPageSize';
         DELETE FROM globalconfig WHERE 
             property = 'popcard.media.videosPageSize';
         DELETE FROM globalconfig WHERE 
             property = 'popcard.media.bookmarksPageSize';
         DELETE FROM globalconfig WHERE 
             property = 'popcard.media.ranksPageSize';
    """),
]
