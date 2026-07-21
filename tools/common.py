"""
DraftGen Common Diagnostic Utilities

Shared utilities used by every DraftGen diagnostic tool.

Every milestone test imports this file instead of
duplicating setup code.
"""

import sys
import platform
import importlib
import pcbnew

# ----------------------------------------------------------
# Project Configuration
# ----------------------------------------------------------

PROJECT_ROOT = r"C:\Projects\DraftGen"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ----------------------------------------------------------
# Import DraftGen Modules
# ----------------------------------------------------------

import draftgen.board
import draftgen.kicad_io

import draftgen.geometry
import draftgen.geometry_io

import draftgen.footprint
import draftgen.footprint_io

# ----------------------------------------------------------
# Reload Modules
# ----------------------------------------------------------

def reload_modules():
    """
    Reload all DraftGen modules.

    Allows testing without restarting KiCad.
    """

    importlib.reload(draftgen.board)
    importlib.reload(draftgen.kicad_io)

    importlib.reload(draftgen.geometry)
    importlib.reload(draftgen.geometry_io)

    importlib.reload(draftgen.footprint)
    importlib.reload(draftgen.footprint_io)


# Always reload when imported
reload_modules()

# ----------------------------------------------------------
# Import Public APIs
# ----------------------------------------------------------

from draftgen.kicad_io import load_board_data
from draftgen.geometry_io import load_geometry
from draftgen.footprint_io import load_footprints

# ----------------------------------------------------------
# Console Helpers
# ----------------------------------------------------------

LINE = "=" * 60
SECTION = "-" * 30


def separator():
    print(LINE)


def section(title):
    print(title)
    print(SECTION)


def blank():
    print()


# ----------------------------------------------------------
# Banner
# ----------------------------------------------------------

def banner(title):
    separator()
    print(title)
    separator()


# ----------------------------------------------------------
# Environment
# ----------------------------------------------------------

def print_environment():

    print(f"KiCad Version : {pcbnew.Version()}")
    print(f"Python        : {sys.version.split()[0]}")
    print(f"Platform      : {platform.system()}")

    blank()


# ----------------------------------------------------------
# Status Helpers
# ----------------------------------------------------------

def pass_msg(message):
    print(f"PASS : {message}")


def fail_msg(message):
    print(f"FAIL : {message}")


def warn_msg(message):
    print(f"WARN : {message}")


# ----------------------------------------------------------
# Final Status
# ----------------------------------------------------------

def status_ready():

    separator()
    print("STATUS : READY")
    separator()


def status_failed():

    separator()
    print("STATUS : FAILED")
    separator()


# ----------------------------------------------------------
# Simple Object Counter
# ----------------------------------------------------------

def count(iterable):
    """
    Safe counter for generators and lists.
    """

    return sum(1 for _ in iterable)