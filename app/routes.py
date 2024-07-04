from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.forms import PlayerForm, GameForm, PlayerStatsForm
from app.models import Player, Game, PlayerStats

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
    players = Player.query.all()
    players_sorted = sorted(players, key=lambda player: player.batting_average, reverse=True)
    games = Game.query.all()
    return render_template('index.html', players=players_sorted, games=games)


@bp.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(name=form.name.data)
        db.session.add(player)
        db.session.commit()
        flash('Player added!')
        return redirect(url_for('routes.index'))
    return render_template('player.html', form=form)


@bp.route('/add_game', methods=['GET', 'POST'])
def add_game():
    form = GameForm()
    if form.validate_on_submit():
        game = Game(date=form.date.data, opponent=form.opponent.data,
                    score_own=form.score_own.data, score_opponent=form.score_opponent.data)
        db.session.add(game)
        db.session.commit()
        flash('Game added!')
        return redirect(url_for('routes.index'))
    return render_template('game.html', form=form)


@bp.route('/add_player_stats/<int:game_id>', methods=['GET', 'POST'])
def add_player_stats(game_id):
    form = PlayerStatsForm()
    form.player.choices = [(p.id, p.name) for p in Player.query.all()]
    if form.validate_on_submit():
        player_stats = PlayerStats(player_id=form.player.data, game_id=game_id,
                                   singles=form.singles.data, doubles=form.doubles.data,
                                   triples=form.triples.data, home_runs=form.home_runs.data,
                                   walks=form.walks.data, outs=form.outs.data,
                                   position=form.position.data)  # Handle position
        db.session.add(player_stats)
        db.session.commit()

        # Update player's season stats
        player = Player.query.get(form.player.data)
        player.update_stats()
        db.session.commit()

        flash('Stats added and season stats updated!')
        return redirect(url_for('routes.index'))
    return render_template('player_stats.html', form=form)


@bp.route('/stats')
def stats():
    players = Player.query.all()
    players_sorted = sorted(players, key=lambda player: player.batting_average, reverse=True)
    return render_template('stats.html', players=players_sorted)


@bp.route('/game_stats/<int:game_id>')
def game_stats(game_id):
    game = Game.query.get_or_404(game_id)
    player_stats = PlayerStats.query.filter_by(game_id=game.id).all()
    return render_template('game_stats.html', game=game, player_stats=player_stats)


@bp.route('/delete_player_stats/<int:player_stats_id>', methods=['POST'])
def delete_player_stats(player_stats_id):
    player_stats = PlayerStats.query.get_or_404(player_stats_id)
    player = player_stats.player
    db.session.delete(player_stats)
    db.session.commit()

    # Update player's season stats after deletion
    player.update_stats()
    db.session.commit()

    flash('Player stats deleted and season stats updated!')
    return redirect(url_for('routes.game_stats', game_id=player_stats.game_id))


@bp.route('/delete_game/<int:game_id>', methods=['GET', 'POST'])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    if request.method == 'POST':
        # Delete associated player stats
        player_stats = PlayerStats.query.filter_by(game_id=game.id).all()
        for stats in player_stats:
            player = stats.player
            db.session.delete(stats)
            player.update_stats()
            db.session.commit()

        db.session.delete(game)
        db.session.commit()
        flash('Game and associated player stats have been deleted!')
        return redirect(url_for('routes.index'))
    return render_template('delete_game.html', game=game)
