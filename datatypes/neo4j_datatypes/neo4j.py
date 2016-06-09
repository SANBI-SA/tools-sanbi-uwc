"""
Neo4j Composite Dataset
"""
import logging
import sys

from galaxy.datatypes.images import Html
from galaxy.datatypes.data import Data, Text
from galaxy.datatypes.metadata import MetadataElement
import shutil
import os

gal_Log = logging.getLogger(__name__)
verbose = True


class Neo4j(Html):
    """
    base class to use for neostore datatypes
    derived from html - composite datatype elements
    stored in extra files path
    """
    MetadataElement( name='neostore', default=None, desc='Neo4j NeoStore File', readonly=True, visible=True, set_in_upload=True, no_value=None )
    MetadataElement( name='neostore_count_file', default=None, desc='Neo4j Count File', readonly=True, visible=True, set_in_upload=True, no_value=None )
    MetadataElement( name="neostore_labeltokenstore_db_file", default=None, desc="Neostore LabelTokenStore File", readonly=True, visible=True, no_value=None )
    MetadataElement( name="neostore_nodestore_file", default=None, desc="Neostore NodeStore File", readonly=True, visible=True, no_value=None)
    MetadataElement( name="neostore_propertystore_file", default=None, desc="Neostore Property Store File", readonly=True, visible=True, no_value=None)
    MetadataElement( name="neostore_relationship_group_file", default=None, desc="Neostore Relationship Group File", readonly=True, visible=True, no_value=None)
    MetadataElement( name="neostore_relationship_file", default=None, desc="Neostore Relationship File", readonly=True, visible=True, no_value=None)
    MetadataElement( name="neostore_relationship_type_file", default=None, desc="Neostore Relationship Type File", readonly=True, visible=True, no_value=None)
    MetadataElement( name="neostore_schema_store_file", default=None, desc="Neostore Schema Store File", readonly=True, visible=True, no_value=None)
    MetadataElement( name="neostore_transaction_db_file", default=None, desc="Neostore Transaction File", readonly=True, visible=True, no_value=None)

    def get_mime(self):
        """Returns the mime type of the datatype"""
        return 'text/html'

    def set_peek(self, dataset, is_multi_byte=False):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = 'Neo4j database (multiple files)'
            dataset.blurb = 'Neo4j database (multiple files)'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def display_peek(self, dataset):
        """Create HTML content, used for displaying peek."""
        try:
            return dataset.peek
        except Exception:
            return "NEO4J database (multiple files)"

    def display_data(self, trans, data, preview=False, filename=None,
                     to_ext=None, size=None, offset=None, **kwd):
        """Documented as an old display method, but still gets called via tests etc
        This allows us to format the data shown in the central pane via the "eye" icon.
        """
        trans.response.set_content_type(data.get_mime())
        trans.log_event( "Display dataset id: %s" % str( data.id ) )

        # the target directory name
        dir_name = str(os.path.dirname( trans.app.object_store.get_filename(data.dataset) )) + '/dataset_{}_files/neo4jdb'.format( data.dataset.id )

        # generate unique filename for this dataset
        valid_chars = '.,^_-()[]0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        fname = ''.join(c in valid_chars and c or '_' for c in data.name)[0:150]

        # zip the target directory (dir_name) using the fname
        shutil.make_archive(fname, 'zip', dir_name)
        download_zip = fname + '.zip'

        # setup headers for the download
        trans.response.headers['Content-Length'] = int( os.stat( download_zip ).st_size )
        trans.response.set_content_type( "application/octet-stream" )  # force octet-stream so Safari doesn't append mime extensions to filename
        trans.response.headers["Content-Disposition"] = 'attachment; filename="Galaxy%s-[%s].%s"' % (data.hid, download_zip , "zip")

        return open( download_zip )

class Neo4jDB(Neo4j, Data):
    """Class for neo4jDB database files."""
    file_ext = 'neostore'
    composite_type = 'basic'
    allow_datatype_change = False


    def __init__(self, **kwd):
        Data.__init__(self, **kwd)
        self.add_composite_file('neostore', substitute_name_with_metadata='neostore', is_binary=True)
        self.add_composite_file('neostore.id', substitute_name_with_metadata='neostore', is_binary=True)
        self.add_composite_file('neostore.counts.db.a', substitute_name_with_metadata='neostore_count_file', is_binary=True)
        self.add_composite_file('neostore.counts.db.b', substitute_name_with_metadata='neostore_count_file', is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db', substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db.id', substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db.names', substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.labeltokenstore.db.names.id', substitute_name_with_metadata='neostore_labeltokenstore_db_file', is_binary=True)
        self.add_composite_file('neostore.nodestore.db', substitute_name_with_metadata='neostore_nodestore_file', is_binary=True)
        self.add_composite_file('neostore.nodestore.db.id', substitute_name_with_metadata='neostore_nodestore_file', is_binary=True)
        self.add_composite_file('neostore.nodestore.db.labels', substitute_name_with_metadata='neostore_nodestore_file', is_binary=True)
        self.add_composite_file('neostore.nodestore.db.labels.id', substitute_name_with_metadata='neostore_nodestore_file', is_binary=True)

        self.add_composite_file('neostore.propertystore.db', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.id', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.arrays', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.arrays.id', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index.id', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index.keys', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.index.keys.id', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.strings', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)
        self.add_composite_file('neostore.propertystore.db.strings.id', substitute_name_with_metadata='neostore_propertystore_file', is_binary=True)

        self.add_composite_file('neostore.relationshipgroupstore.db', substitute_name_with_metadata='neostore_relationship_group_file', is_binary=True)
        self.add_composite_file('neostore.relationshipgroupstore.db.id', substitute_name_with_metadata='neostore_relationship_group_file', is_binary=True)
        self.add_composite_file('neostore.relationshipstore.db', substitute_name_with_metadata='neostore_relationship_file', is_binary=True)
        self.add_composite_file('neostore.relationshipstore.db.id', substitute_name_with_metadata='neostore_relationship_file', is_binary=True)
        self.add_composite_file('neostore.relationshiptypestore.db.names', substitute_name_with_metadata='neostore_relationship_type_file', is_binary=True)
        self.add_composite_file('neostore.relationshiptypestore.db.names.id', substitute_name_with_metadata='neostore_relationship_type_file', is_binary=True)
        self.add_composite_file('neostore.schemastore.db', substitute_name_with_metadata='neostore_schema_store_file', is_binary=True)
        self.add_composite_file('neostore.schemastore.db.id', substitute_name_with_metadata='neostore_schema_store_file', is_binary=True)
        self.add_composite_file('neostore.transaction.db.0', substitute_name_with_metadata='neostore_count_file', is_binary=True)


if __name__ == '__main__':
    import doctest
    doctest.testmod(sys.modules[__name__])