"""
Neo4j Composite Dataset
"""
import logging
import sys
import os

from galaxy.datatypes.images import Html
from galaxy.datatypes.data import Data, Text
from galaxy.datatypes.metadata import MetadataElement

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

    composite_type = 'auto_primary_file'
    allow_datatype_change = False
    file_ext = 'neo4j'

    def generate_primary_file( self, dataset=None ):
        rval = ['<html><head><title>Neo4j Galaxy Composite Dataset </title></head><p/>']
        rval.append('<div>This composite dataset is composed of the following files:<p/><ul>')
        for composite_name, composite_file in self.get_composite_files( dataset=dataset ).iteritems():
            fn = composite_name
            opt_text = ''
            if composite_file.optional:
                opt_text = ' (optional)'
            if composite_file.get('description'):
                rval.append( '<li><a href="%s" type="application/binary">%s (%s)</a>%s</li>' % ( fn, fn, composite_file.get('description'), opt_text ) )
            else:
                rval.append( '<li><a href="%s" type="application/binary">%s</a>%s</li>' % ( fn, fn, opt_text ) )
        rval.append( '</ul></div></html>' )
        return "\n".join( rval )

    def regenerate_primary_file(self, dataset):
        """
        cannot do this until we are setting metadata
        """
        efp = dataset.extra_files_path
        flist = os.listdir(efp)
        rval = ['<html><head><title>Files for Composite Dataset %s</title></head><body><p/>Composite %s contains:<p/><ul>' % (dataset.name, dataset.name)]
        for i, fname in enumerate(flist):
            sfname = os.path.split(fname)[-1]
            f, e = os.path.splitext(fname)
            rval.append( '<li><a href="%s">%s</a></li>' % ( sfname, sfname) )
        rval.append( '</ul></body></html>' )
        f = file(dataset.file_name, 'w')
        f.write("\n".join( rval ))
        f.write('\n')
        f.close()


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
        if filename is not None and filename != "index":
            # Change nothing - important for the unit tests to access child files:
            return Data.display_data(self, trans, data, preview, filename,
                                     to_ext, size, offset, **kwd)
        if self.file_ext == "neostore":
            title = "This is a NEO4J database"
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


class Neo4jDB(Neo4j, Data):
    """Class for neo4jDB database files."""
    file_ext = 'neostore'

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