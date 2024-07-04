from datetime import datetime
from app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    singles = db.Column(db.Integer, default=0)
    doubles = db.Column(db.Integer, default=0)
    triples = db.Column(db.Integer, default=0)
    home_runs = db.Column(db.Integer, default=0)
    walks = db.Column(db.Integer, default=0)
    outs = db.Column(db.Integer, default=0)
    player_stats = db.relationship('PlayerStats', backref='player', lazy=True)

    @property
    def batting_average(self):
        at_bats = self.singles + self.doubles + self.triples + self.home_runs + self.outs
        if at_bats == 0:
            return 0
        hits = self.singles + self.doubles + self.triples + self.home_runs
        return hits / at_bats

    @property
    def slugging_percentage(self):
        at_bats = self.singles + self.doubles + self.triples + self.home_runs + self.outs
        if at_bats == 0:
            return 0
        total_bases = self.singles + 2 * self.doubles + 3 * self.triples + 4 * self.home_runs
        return total_bases / at_bats

    def update_stats(self):
        self.singles = sum(stat.singles for stat in self.player_stats)
        self.doubles = sum(stat.doubles for stat in self.player_stats)
        self.triples = sum(stat.triples for stat in self.player_stats)
        self.home_runs = sum(stat.home_runs for stat in self.player_stats)
        self.walks = sum(stat.walks for stat in self.player_stats)
        self.outs = sum(stat.outs for stat in self.player_stats)
        db.session.commit()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    opponent = db.Column(db.String(64))
    score_own = db.Column(db.Integer, default=0, nullable=True)
    score_opponent = db.Column(db.Integer, default=0, nullable=True)
    players = db.relationship('PlayerStats', backref='game', lazy=True)

class PlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    singles = db.Column(db.Integer, default=0)
    doubles = db.Column(db.Integer, default=0)
    triples = db.Column(db.Integer, default=0)
    home_runs = db.Column(db.Integer, default=0)
    walks = db.Column(db.Integer, default=0)
    outs = db.Column(db.Integer, default=0)
    position = db.Column(db.String(20))  # Add position field
