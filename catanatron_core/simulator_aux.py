from our_accumulators import CompletaAccumulator, EvaluateBots
from catanatron_experimental.cli.simulation_accumulator import SimulationAccumulator
from catanatron.models.map import build_map
from catanatron.game import Game
from catanatron.models.player import Color
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich import box
from rich.console import Console
from rich.theme import Theme
from rich.text import Text
from catanatron_experimental.cli.accumulators import VpDistributionAccumulator, StatisticsAccumulator
import json, random

COLOR_TO_RICH_STYLE = {
    Color.RED: "red",
    Color.BLUE: "blue",
    Color.ORANGE: "yellow",
    Color.WHITE: "white",
}

def rich_color(color):
    if color is None:
        return ""
    style = COLOR_TO_RICH_STYLE[color]
    return f"[{style}]{color.value}[/{style}]"

def rich_player_name(player):
    style = COLOR_TO_RICH_STYLE[player.color]
    return f"[{style}]{player}[/{style}]"

custom_theme = Theme(
    {
        "progress.remaining": "",
        "progress.percentage": "",
        "bar.complete": "green",
        "bar.finished": "green",
    }
)
console = Console(theme=custom_theme)

class CustomTimeRemainingColumn(TimeRemainingColumn):
    """Renders estimated time remaining according to show_time field."""

    def render(self, task):
        """Show time remaining."""
        show = task.fields.get("show_time", True)
        if not show:
            return Text("")
        return super().render(task)


def play_batch_core(num_games, players, accumulators=[]):
    for accumulator in accumulators:
        if isinstance(accumulator, SimulationAccumulator):
            accumulator.before_all()

    for _ in range(num_games):
        for player in players:
            player.reset_state()
        catan_map = build_map("BASE")
        game = Game(
            players,
            discard_limit=7,
            vps_to_win=10,
            catan_map=catan_map,
        )
        game.play(accumulators)
        yield game

    for accumulator in accumulators:
        if isinstance(accumulator, SimulationAccumulator):
            accumulator.after_all()

def play_batch(num_games, players, statistics=False, all_data=False):
    vp_accumulator = VpDistributionAccumulator()
    statistics_accumulator = StatisticsAccumulator()
    evaluate_bots = EvaluateBots()
    accumulators = [evaluate_bots, vp_accumulator, statistics_accumulator]
    if all_data:
        getdata = CompletaAccumulator()
        accumulators.append(getdata)

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        CustomTimeRemainingColumn(),
        console=console,
    ) as progress:
        main_task = progress.add_task(f"Playing {num_games} games...", total=num_games)
        player_tasks = [
            progress.add_task(
                rich_player_name(player), total=num_games, show_time=False
            )
            for player in players
        ]

        for i, game in enumerate(
            play_batch_core(num_games, players, accumulators)
        ):
            winning_color = game.winning_color()

            progress.update(main_task, advance=1)
            if winning_color is not None:
                winning_index = list(map(lambda p: p.color, players)).index(
                    winning_color
                )
                winner_task = player_tasks[winning_index]
                progress.update(winner_task, advance=1)
        progress.refresh()
    results = {
      'cities': str(vp_accumulator.cities),
      'settlements': str(vp_accumulator.settlements),
      'devvps': str(vp_accumulator.devvps),
      'longest': str(vp_accumulator.longest),
      'largest': str(vp_accumulator.largest),
    }
    # batchid = './simulations' + ''.join(random.choices('0123456789', k=5)) + '.json'
    # with open(batchid, 'w') as f:
    #     json.dump(results, f, indent=4)
    if statistics:
        return statistics_accumulator, vp_accumulator
    return evaluate_bots.final_df