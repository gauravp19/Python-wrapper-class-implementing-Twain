import twain
import os
import datetime


class Scanner(object):

    source_object = None
    source = None
    current_destination_directory = None
    current_scanner = None

    def __init__(self):
        pass

    @staticmethod
    def initialize_scanner():
        Scanner.source_object = twain.SourceManager(0)

    @staticmethod
    def get_list_of_available_scanners():
        return Scanner.source_object.GetSourceList()

    @staticmethod
    def set_scanner(scanner_name, dpi):
        try:
            Scanner.source = Scanner.source_object.OpenSource(scanner_name)
            if Scanner.source is not None:
                Scanner.source.SetCapability(twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(dpi))
                Scanner.source.SetCapability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(dpi))
                Scanner.source.SetCapability(twain.CAP_FEEDERENABLED, twain.TWTY_FIX32, float(dpi))
                Scanner.source.SetCapability(twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, twain.TWPT_BW)
                Scanner.source.RequestAcquire(0, 0)
            else:
                print "No source selected"
        except twain.excTWCC_SUCCESS:
            print "No source selected"

    @staticmethod
    def scan(destination_directory):
        Scanner.current_destination_directory = destination_directory
        try:
            while True:

                raw_file = Scanner.source.XferImageNatively()
                if raw_file:
                    (handle, count) = raw_file
                    new_file = os.path.join(destination_directory,
                                            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".bmp")
                    twain.DIBToBMFile(handle, new_file)
        except twain.excDSTransferCancelled:
            print "There is/are no paper/papers in the feeder!"
        except twain.excTWCC_SEQERROR:
            Scanner.close_source()
            print "All the documents have been successfully scanned"
        except twain.excTWCC_BUMMER:
            print "Paper Jammed!"

    @staticmethod
    def close_source():
        Scanner.source.destroy()
        Scanner.source_object.destroy()
        Scanner.source = None
        Scanner.source_object = None

