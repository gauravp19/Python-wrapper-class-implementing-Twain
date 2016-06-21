# Python-wrapper-class-implementing-Twain (Updated to have allow custom DPI)

_Scanner = Scanner()

scannerObj = _Scanner.get_sources()

_Scanner.open_sources(scannerObj)

_Scanner.start_scan("Dest Directory")
