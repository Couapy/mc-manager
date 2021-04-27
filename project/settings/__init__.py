import sys

from .base import *

if 'test' in sys.argv:
    from .dev import *
else:
    from .prod import *

sys.path.insert(0, BASE_DIR + '/apps')
