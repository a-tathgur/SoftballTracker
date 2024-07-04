"""
from app import create_app, db
from app.models import Player, PlayerStats, Game

def reset_db_all():
    #Reset the database by dropping and recreating all tables.
    db.drop_all()
    db.create_all()
    print("Database has been reset!")

def reset_db_data():
    #Clear all data from the database.
    PlayerStats.query.delete()
    Game.query.delete()
    Player.query.delete()
    db.session.commit()
    print("All data has been cleared from the database!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        reset_db_all()  # or reset_db_data()
"""