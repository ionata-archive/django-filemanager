{% load url from future %}
/*---------------------------------------------------------
  Configuration
---------------------------------------------------------*/

// Set this to the server side language you wish to use.
var lang = 'py'; // options: lasso, php, py

// Set this to the directory you wish to manage.
var fileRoot = '{{ UPLOAD_URL }}';

// Show image previews in grid views?
var showThumbs = true;

var django_view = '{% url "filemanager" %}';
