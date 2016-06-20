import twain
import shutil
import os
import datetime


class Scanner(object):
    """The documentation of this class follows PEP-257 Docstring conventions
    This class is demonstrated the basic capabilities of the twain's python extension.
    It is important to have the twain.pyd as well as the pytwain module imported before testing
    the implementation of this class. The only other non standard library is the PythonMagick used
    for conversion and compression of scanned images. The PythonMagick module is not compiled from source
    but is retrieved from the website serving the unofficial python binaries for various libraries in python
    The whl file was extracted using PIP.
    """

    get_source_object = None
    open_source = None
    recently_created_directory = None

    def __init__(self):
        pass

    @staticmethod
    def get_sources():
        """This method returns the Source Object"""
        Scanner.get_source_object = twain.SourceManager(0)
        return Scanner.get_source_object

    @staticmethod
    def open_sources(obj):
        """This method displays the list of connected scanners in some cases it displays one device as two different
        devices this is primarily because it is capable of using the vendor provided drivers along with generic twain
         drivers to communicate with the hardware. Once the user selects his preferred device the method calls the
         native interface providing options for selecting the page dimensions, setting DPI, and option to select
         Flatbed or Feeder mode"""
        if type(Scanner.get_source_object) == type(obj):
            try:
                Scanner.open_source = obj.OpenSource()
                if Scanner.open_source is not None:
                    Scanner.open_source.RequestAcquire(1, 1)
                else:
                    print "No source selected"
            except twain.excTWCC_SUCCESS:
                print "No source selected"
        else:
            print "Invalid source object passed"

    @staticmethod
    def start_scan(destination_directory):
        """This method gets the document from he scanner when it completes scanning it also creates a directory in the
        root folder of the code where it stores them later it moves the images to a desired location on the disk
        based on the argument passed to this method. Shutil is used instead of native os file transfers as shutil overcomes
        the problem related to moving files to different disks"""
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




