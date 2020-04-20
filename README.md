# pyplanet-best_times
Simple Plugin for PyPlanet to have an overview of the best 12 Times.
Also possible to get a detailed view of all times driven this round with differences to the best time.

##Installation
Copy the `best_times` folder to your `/pyplanet/apps/` folder.

Add the app in the `/pyplanet/settings/apps.py` Apps file with `'apps.best_times',`.

Or like this:

    APPS = {
	'default': [
		//'pyplanet.apps.contrib.*', My Other apps
		'apps.best_times',
	 ]
    }

##Preview

![Overview of best 12 times!](https://raw.githubusercontent.com/Lmbwilly/pyplanet-best_times/master/top12.png "Overview of best 12 times")

![Detailed list of all times!](https://raw.githubusercontent.com/Lmbwilly/pyplanet-best_times/master/list.png "Detailed list of all time")
