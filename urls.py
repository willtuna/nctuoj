from handler import Handler

urls = [
    ('/', Handler.Index),
    ('/api/missions/', Handler.api.Missions),
    ('/api/judge/', Handler.api.Judge),
    ('.*', Handler.NotFound),
]
