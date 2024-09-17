# Sans-Pipe Maya Light Pipeline Utility - Toolkit

"""
This tool kit stores the functions that help run the SANS-PIPE UTILITY.  The idea here is that these tools can be used
in or out of the pipeline system, with, or without the main UI.
"""

from maya import cmds
import os
import sys
import re
import json
import time
from datetime import datetime


class sp_toolkit(object):
    def __init__(self):
        print('SHIT WORKED!!')
