"""
CtbReports Composite Dataset
"""
import logging
import sys

from galaxy.datatypes.data import Data
#from galaxy.datatypes.images import Html

gal_Log = logging.getLogger(__name__)
verbose = True


class CtbReport(object):
    """
    base class to use for cbtreports datatypes
    derived from html - composite datatype elements
    stored in extra files path
    """

    def get_mime(self):
        """Returns the mime type of the datatype"""
        return 'text/html'

    def set_peek(self, dataset, is_multi_byte=False):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = 'CtbReports (multiple files)'
            dataset.blurb = 'CtbReports (multiple files)'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def display_peek(self, dataset):
        """Create HTML content, used for displaying peek."""
        try:
            return dataset.peek
        except Exception:
            return "CtbReports (multiple files)"

    def display_data(self, trans, data, preview=False, filename=None,
                     to_ext=None, size=None, offset=None, **kwd):
        """Documented as an old display method, but still gets called via tests etc
        This allows us to format the data shown in the central pane via the "eye" icon.
        """
        if filename is not None and filename != "index":
            # Change nothing - important for the unit tests to access child files:
            return Data.display_data(self, trans, data, preview, filename,
                                     to_ext, size, offset, **kwd)
        if self.file_ext == "ctbreport":
            title = "This is a CtbReports database"
        msg = ""
        try:
            # Try to use any text recorded in the dummy index file:
            handle = open(data.file_name, "rU")
            msg = handle.read().strip()
            handle.close()
        except Exception:
            pass
        if not msg:
            msg = title
        # Galaxy assumes HTML for the display of composite datatypes,
        return "<html><head><title>%s</title></head><body><pre>%s</pre></body></html>" % (title, msg)


class CtbReportSet(CtbReport, Data):
    """Class for Ctb Report Set files."""
    file_ext = 'ctbreport'
    composite_type = 'basic'
    allow_datatype_change = False

    def __init__(self, **kwd):
        Data.__init__(self, **kwd)
        self.add_composite_file('neo4j/', is_binary=True)
        self.add_composite_file('jbrowser/', is_binary=True)
