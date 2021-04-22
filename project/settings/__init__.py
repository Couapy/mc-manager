import sys

from .base import *
# from .dev import *
from .prod import *

sys.path.insert(0, BASE_DIR + '/apps')
