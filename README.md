django-filemanager
======================

A Django app that wraps [Filemanager][] from [Core Five Labs][c5l], adding lots
of Djangoy goodness

Installing
----------

Install the package:

    pip install django-filemanager

Add it to your installed apps

	INSTALLED_APPS += (
		'filemanager',
	)

Set a few config options:

	FILEMANAGER_UPLOAD_ROOT = MEDIA_ROOT + 'uploads/'
	FILEMANAGER_UPLOAD_URL = MEDIA_URL + 'uploads/'

And include its URLs:

	# in urls.py

	urlpatterns += patterns("",
		(r"^filemanager/", include("filemanager.urls")),
	)

Now, send a user to `/filemanager/` and they will be able to manage file
uploads on the server.
