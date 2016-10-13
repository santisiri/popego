__docformat__ = "restructuredtext"

migration = [
    ("""\
         UPDATE services 
           SET agent = 'popserver.agents.twitter_agent'
           WHERE name = 'Twitter';
         
      """,
    """\
         UPDATE services 
           SET agent = 'popserver.agents.twitter_agent:TwitterAgent()'
           WHERE name = 'Twitter';
    """),
]
