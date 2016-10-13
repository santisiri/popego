""" ServiceType 'photos' a 'pictures' """

__docformat__ = "restructuredtext"


# I'm using a creative whitespace style that makes it readable both here
# and when printed.

migration = [
    ("""\
        UPDATE service_types SET type='pictures' where type='photos';
        """, 
     """\
        UPDATE service_types SET type='photos' where type='pictures';
    """),
]
