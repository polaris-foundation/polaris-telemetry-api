from flask_batteries_included.sqldb import db


def reset_database() -> None:

    session = db.session

    session.execute("TRUNCATE TABLE mobile cascade")
    session.execute("TRUNCATE TABLE desktop cascade")
    session.commit()

    session.close()
