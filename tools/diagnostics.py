"""
DraftGen Diagnostics

Usage:

Inside KiCad:
    python diagnostics.py

Outside KiCad:
    python diagnostics.py "C:\\Projects\\MyBoard\\MyBoard.kicad_pcb"
"""

import sys
import platform
import pcbnew


def separator():
    print("=" * 60)


def get_board():
    """
    Returns a BOARD object.

    Priority:
        1. Load board from command-line argument
        2. Use currently opened board (Plugin/Console)
    """

    # Command line mode
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print(f"Loading board from:\n{filename}\n")
        return pcbnew.LoadBoard(filename)

    # KiCad Plugin / KiPython mode
    return pcbnew.GetBoard()


def main():

    separator()
    print("DraftGen Diagnostics")
    separator()

    print(f"KiCad Version : {pcbnew.Version()}")
    print(f"Python        : {sys.version.split()[0]}")
    print(f"Platform      : {platform.system()}")

    print()

    board = get_board()

    if board is None:
        print("ERROR: No board available.")
        print()
        print("Run one of the following:")
        print()
        print("1. Inside KiCad (Plugin / KiPython)")
        print("2. diagnostics.py <board.kicad_pcb>")
        return

    print("Board Loaded Successfully")
    print()

    print(f"Project File  : {board.GetFileName()}")
    print(f"Copper Layers : {board.GetCopperLayerCount()}")

    separator()
    print("STATUS : READY")
    separator()


if __name__ == "__main__":
    main()