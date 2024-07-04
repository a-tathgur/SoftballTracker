from app import create_app, db
from app.models import Player, Game, PlayerStats

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Player': Player, 'Game': Game, 'PlayerStats': PlayerStats}


if __name__ == '__main__':
    app.run(debug=True)
