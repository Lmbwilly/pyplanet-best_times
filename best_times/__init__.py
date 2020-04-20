import asyncio

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from .view import BestTimesWidget
from .view import TimesListView


class BestTimesApp(AppConfig):
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']
	# mode_dependencies = ['TimeAttack']

	best_times = []

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.number_of_checkpoints = None
		self.best_times = []  # List of PlayerTime Objects
		self.widget = None

	async def on_start(self):
		self.context.signals.listen(tm_signals.finish, self.player_finish)
		self.context.signals.listen(mp_signals.player.player_connect, self.player_connect)
		self.context.signals.listen(mp_signals.map.map_begin, self.map_begin)
		self.context.signals.listen(mp_signals.map.map_start__end, self.map_end)
		self.best_times.clear()
		self.widget = BestTimesWidget(self)
		asyncio.ensure_future(self.widget.display())

	# When a player passes a CP
	async def player_finish(self, player, lap_time, *args, **kwargs):
		laptime = lap_time
		pt = PlayerTime(player, laptime)
		if not self.best_times:
			self.best_times.append(pt)
		else:
			added = False
			for idx, current_time in enumerate(self.best_times):
				if pt.time < current_time.time:
					self.best_times.insert(idx, pt)
					added = True
					break
			if not added:
				self.best_times.append(pt)
		await self.widget.display()

	# When the map starts
	async def map_begin(self, *args, **kwargs):
		self.best_times.clear()
		await self.widget.display()

	# When the map ends. This is needed to not keep the old times data when the map is restarted.
	async def map_end(self, *args, **kwargs):
		self.best_times.clear()
		await self.widget.display()

	# When a player connects
	async def player_connect(self, player, **kwargs):
		await self.widget.display(player)


# PlayerTime Event mapping a player to a time
class PlayerTime:
	def __init__(self, player, time=0):
		self.player = player
		self.time = time