from bibliophiliac.views import database

def test_database_connection(app):
    db = database.access_database()
    assert db is database.access_database()
    database.close_db()
    assert db is not database.access_database()

def test_initialize_command(runner, monkeypatch):
    class RanCommand(object):
        did_run = False 

    def is_running():
        RanCommand.did_run = True

    monkeypatch.setattr('bibliophiliac.views.database.initialize_database', is_running)
    runner.invoke(args=['initialize-database'])
    assert RanCommand.did_run

