__docformat__ = "restructuredtext"

migration = [
    ("""\
         UPDATE services SET prompt_text = 'username or email:' WHERE name = 'Flickr'
      """,
    """\
         UPDATE services SET prompt_text = 'username:' WHERE name = 'Flickr'
    """),
]
