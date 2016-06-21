import twain
import shutil
import os
import datetime


class Scanner(object):
    """
    The documentation of this class follows PEP 257 Docstring conventions.
    This is a wrapper class implementing the Twain which is a API for
    accessing Scanner and Camera on a windows machine. The purpose of this
    class is to provide an easy access to the code present within the twain.pyd
    file that can be downloaded from https://pypi.python.org/pypi/twain the aforementioned
    file is a DLL file. The twain file supports 32-bit Windows and does not support Linux or
    OSx.
    """
    # Global static variables
    get_source_object = None
    open_source = None
    recently_created_directory = None
    dpi = 600

    def __init__(self):
        pass

    @staticmethod
    def get_sources():
        """
        The purpose of this method is to retrieve the the source object
        :return: Source object
        """
        Scanner.get_source_object = twain.SourceManager(0)
        return Scanner.get_source_object

    @staticmethod
    def open_sources(obj):
        """
        The source object returned by the get_sources method is passed as a parameter
        to the open_sources method. This method when called displays the list of connected
        scanners in some cases it displays two devices even though only one device is connected
        to the computer the aforementioned is because twain has its own set of drivers that can
        talk to the scanner/camera hardware. Once the user selects a source (preferred device)
        the program then calls the native scanner interface that provides options related to
        page size and feeder or flat bed selection. This class is designed keeping the process of
        automation during the usage of a feeder in mind.
        :param obj: Source Object
        :return: -
        """
        if type(Scanner.get_source_object) == type(obj):
            try:
                sourceList = obj.GetSourceList()
                Scanner.open_source = obj.OpenSource(sourceList[0])
                if Scanner.open_source is not None:
                    Scanner.open_source.SetCapability(twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(Scanner.dpi))
                    Scanner.open_source.SetCapability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(Scanner.dpi))
                    Scanner.open_source.SetCapability(twain.CAP_FEEDERENABLED,twain.TWTY_FIX32, float(Scanner.dpi))
                    Scanner.open_source.RequestAcquire(0, 0)
                else:
                    print "No source selected"
            except twain.excTWCC_SUCCESS:
                print "No source selected"
        else:
            print "Invalid source object passed"

    @staticmethod
    def start_scan(destination_directory):
        """
        This method is called once the source and the preferred scan settings are selected. This method
        retrieves the scanned document from the printer in the form of a .bmp. Initially it stores the files
        in the code directory later it moves them to a timestamped directory at the destination directory.
        The bitmaps obtained are typically very
        large in size.
        :param destination_directory:
        :return: -
        """
        new_directory = os.path.join(destination_directory, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        Scanner.recently_created_directory = new_directory
        os.mkdir(new_directory)
        try:
            counter = 1
            page = "Page"
            bmp = ".bmp"
            while True:
                raw_file = Scanner.open_source.XferImageNatively()
                if raw_file:
                    (handle, count) = raw_file
                    twain.DIBToBMFile(handle, page + str(counter) + str(bmp))
                    counter += 1
                    ls = os.listdir(os.getcwd())
                    for x in ls:
                        name, ext = os.path.splitext(x)
                        if ext.lower() == ".bmp":
                            shutil.move(os.path.join(os.getcwd(), x), os.path.join(new_directory, x))
        except twain.excDSTransferCancelled:
            print "There is/are no paper/papers in the feeder!"
        except twain.excTWCC_SEQERROR:
            print "All the documents have been successfully scanned"
        except twain.excTWCC_BUMMER:
            print "Paper Jammed!"




