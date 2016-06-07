"""
CtbReports Composite Dataset
"""
import logging
import sys

from galaxy.datatypes.data import Data
from galaxy.datatypes.images import Html

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


class CtbReportsNeo4j(CtbReport, Data):
    """Class for neo4jDB database files."""
    file_ext = 'ctbreportneo4j'
    composite_type = 'basic'
    allow_datatype_change = False

    def __init__(self, **kwd):
        Data.__init__(self, **kwd)
        self.add_composite_file('neostore', substitute_name_with_metadata='neostore', is_binary=True)
        self.add_composite_file('neostore.id', substitute_name_with_metadata='neostore', is_binary=True)
        self.add_composite_file('neostore.counts.db.a', substitute_name_with_metadata='neostore_count_file',
                                is_binary=True)
        self.add_composite_file('neostore.counts.db.b', substitute_name_with_metadata='neostore_count_file',
                                is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db',
                                substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db.id',
                                substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db.names',
                                substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db.names.id',
                                substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.nodestore.db', substitute_name_with_metadata='neostore_nodestore_file',
                                is_binary=True)
        self.add_composite_file('neostore.nodestore.db.id', substitute_name_with_metadata='neostore_nodestore_file',
                                is_binary=True)
        self.add_composite_file('neostore.nodestore.db.labels', substitute_name_with_metadata='neostore_nodestore_file',
                                is_binary=True)
        self.add_composite_file('neostore.nodestore.db.labels.id',
                                substitute_name_with_metadata='neostore_nodestore_file', is_binary=True)

        self.add_composite_file('neostore.propertystore.db',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.id',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.arrays',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.arrays.id',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index.id',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index.keys',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index.keys.id',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.strings',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.strings.id',
                                substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)

        self.add_composite_file('neostore.relationshipgroupstore.db',
                                substitute_name_with_metadata='neostore_relationship_group_file', is_binary=True)
        self.add_composite_file('neostore.relationshipgroupstore.db.id',
                                substitute_name_with_metadata='neostore_relationship_group_file', is_binary=True)
        self.add_composite_file('neostore.relationshipstore.db',
                                substitute_name_with_metadata='neostore_relationship_file', is_binary=True)
        self.add_composite_file('neostore.relationshipstore.db.id',
                                substitute_name_with_metadata='neostore_relationship_file', is_binary=True)
        self.add_composite_file('neostore.relationshiptypestore.db.names',
                                substitute_name_with_metadata='neostore_relationship_type_file', is_binary=True)
        self.add_composite_file('neostore.relationshiptypestore.db.names.id',
                                substitute_name_with_metadata='neostore_relationship_type_file', is_binary=True)
        self.add_composite_file('neostore.schemastore.db', substitute_name_with_metadata='neostore_schema_store_file',
                                is_binary=True)
        self.add_composite_file('neostore.schemastore.db.id',
                                substitute_name_with_metadata='neostore_schema_store_file', is_binary=True)
        self.add_composite_file('neostore.transaction.db.0', substitute_name_with_metadata='neostore_count_file',
                                is_binary=True)


class CtbReportsJBrowse(CtbReport, Html):
    """Class for ctb report jbrowse files."""
    file_ext = 'ctbreportjbrowse'
    composite_type = 'basic'
    allow_datatype_change = False

    def __init__(self, **kwd):
        Html.__init__(self, **kwd)


if __name__ == '__main__':
    import doctest

    doctest.testmod(sys.modules[__name__])
