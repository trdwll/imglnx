"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imglnx.settings")

application = get_wsgi_application()
