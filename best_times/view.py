from pyplanet.utils import times
from pyplanet.views.generics.list import ManualListView
from pyplanet.views.generics.widget import TimesWidgetView


class BestTimesWidget(TimesWidgetView):
	widget_x = -124.75
	widget_y = 79
	z_index = 30
	size_x = 250
	size_y = 18
	title = 'Best Times'

	template_name = 'best_times/widget_top.xml'

	def __init__(self, app):
		super().__init__(self)
		self.app = app
		self.manager = app.context.ui
		self.id = 'pyplanet__widget_besttimes'
		self.action = self.action_timeslist

	async def get_all_player_data(self, logins):
		data = await super().get_all_player_data(logins)
		self.logins = []
		pts = {}
		for player in self.app.instance.player_manager.online:
			list_pts = []
			for idx, pt in enumerate(self.app.best_times):
				list_time = {
					'index': idx+1,
					'color': "$0f3" if player.login == pt.player.login else "$ff0",
					'time': times.format_time(pt.time),
					'nickname': pt.player.nickname,
					'login': pt.player.login
				}
				list_pts.append(list_time)
			pts[player.login] = {'pts': list_pts}

		data.update(pts)
		return data

	async def action_timeslist(self, player, **kwargs):
		view = TimesListView(self.app)
		await view.display(player=player.login)
		return view

	# TODO: remove/rework when finishing widget for rounds/cup/team mode gets reworked
	# Only show the widget in TimeAttack mode as it interferes with UI elements in the other modes
	async def display(self, player=None, **kwargs):
		await super().display()
		# current_script = await self.app.instance.mode_manager.get_current_script()
		# if 'TimeAttack' in current_script:
		#
		# else:
		# 	for idx, player in enumerate(self.app.instance.player_manager.online):
		# 		await super().close(player)


class TimesListView(ManualListView):
	title = 'Best Times in current round'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Statistics'

	fields = [
		{
			'name': '#',
			'index': 'index',
			'sorting': True,
			'searching': False,
			'width': 10,
			'type': 'label'
		},
		{
			'name': 'Player',
			'index': 'player_nickname',
			'sorting': False,
			'searching': True,
			'width': 70
		},
		{
			'name': 'Time',
			'index': 'record_time',
			'sorting': True,
			'searching': False,
			'width': 30,
			'type': 'label'
		},
        {
			'name': 'Difference',
			'index': 'record_time_difference',
			'sorting': True,
			'searching': False,
			'width': 50,
			'type': 'label'
		},
	]

	def __init__(self, app):
		super().__init__(self)
		self.app = app
		self.manager = app.context.ui
		self.provide_search = False

	async def get_data(self):
		items = []
		list_times = self.app.best_times
		first_time = list_times[0].time
		for idx, pt in enumerate(list_times):
			time_difference = ''
			if idx > 0:
				time_difference = '$f00 + ' + times.format_time((pt.time - first_time))
			items.append({
				'index': idx+1,
				'player_nickname': pt.player.nickname,
				'record_time': times.format_time(pt.time),
                'record_time_difference': time_difference
			})

		return items
