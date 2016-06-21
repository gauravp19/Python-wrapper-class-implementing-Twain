# Python-wrapper-class-implementing-Twain (Updated to have allow custom DPI)

## Sample code demonstrating the usage of the Document Scanner

## Import Scanner from the file

from DocumentScannerImplementation import Scanner


## Retreive the scanner object
scanner_object = Scanner()

## Display the sources
source = scanner_object.get_sources()

## Open the source
scanner_object.open_sources(source)

## Start scanning
scanner_object.start_scan('destination-directory')
