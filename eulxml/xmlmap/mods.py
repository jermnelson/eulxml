# file eulxml/xmlmap/mods.py
# 
#   Copyright 2011 Colorado College Tutt Library
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
__author__ = 'Jeremy Nelson'
try:
    import rdflib
except ImportError:
    # Follows use rdflib if it's available, but it's ok if it's not
    rdflib = None

from eulxml import xmlmap

class _BaseMODS(xmlmap.XmlObject):
    'Base Library of Congress MODS class for common namespace declarations'
    ROOT_NS = 'http://www.loc.gov/standards/mods/v3/'
    ROOT_NAMESPACES = { 'mods' : ROOT_NS}

class MODSElement(_BaseMODS):
    'Generic MODS with access to element name and value'
    name = xmlmap.StringField('local-name(.)')
    value = xmlmap.StringField('.')

class genre(MODSElement):
    'MODS genre element'
    ROOT_NAME = 'genre'
    authority = xmlmap.StringField('@authority',
                                   choices=["marcgt"])

class identifier(MODSElement):
    'MODS repeatable identifier element'
    ROOT_NAME = 'identifier'
    type = xmlmap.StringField('@type')

class languageTerm(MODSElement):
    'MODS repeatable languageTerm element'
    ROOT_NAME = 'languageTerm'
    type = xmlmap.StringField("@type",
                              choices=["text","code"])

class language(_BaseMODS):
    'MODS language element'
    ROOT_NAME = 'language'
    terms = xmlmap.NodeListField("mods:languageTerm",languageTerm)

class namePart(MODSElement):
    'MODS `namePart` element, child of `name` element.'
    ROOT_NAME = 'namePart'
    type = xmlmap.StringField("@type",
                              choices=["family",
                                       "middle",
                                       "given",
                                       "termsOfAddress"],
                              required=False)

class roleTerm(MODSElement):
    'MODS `roleTerm` element, child of `role` element.'
    ROOT_NAME = 'roleTerm'
    authority = xmlmap.StringField("@authority")
    type = xmlmap.StringField("@type",
                              choices=["code","text"])



class role(_BaseMODS):
    '''MODS role element with child role_term elements'''
    ROOT_NAME = 'role'
    role_term = xmlmap.NodeField('mods:roleTerm',roleTerm)

class name(_BaseMODS):
    'MODS name element'
    ROOT_NAME = 'name'
    display_form = xmlmap.StringField("@displayForm",required=False)
    name_parts = xmlmap.NodeListField("mods:namePart",namePart)
    roles = xmlmap.NodeListField("mods:role",role)
    type = xmlmap.StringField("@type",
                              choices=["personal",
                                       "corporate",
                                       "conference"])


class note(_BaseMODS):
    '''MODS note element'''
    display_label = xmlmap.StringField("@displayLabel")
    "display label - `@displayLabel`"
    type = xmlmap.StringField("@type")
    "free-form type - `@type`"
    value = xmlmap.StringField(".")
    "text content of note node"

class originInfo(_BaseMODS):
    '''MODS originInfo element includes child mods:place, mods:publisher,
       mods:dateIssued, and mods:dateCaptured elements'''
    date_captured = xmlmap.StringField('mods:dateCaptured')
    date_issued = xmlmap.StringField('mods:dateIssued')
    date_issued_keydate = xmlmap.StringField('mods:dateIssued/@keyDate',
                                             choices=["yes","no"])
    place = xmlmap.StringField('mods:place')
    place_term = xmlmap.StringField('mods:place/mods:placeTerm')
    place_term_type = xmlmap.StringField('mods:place/mods:placeTerm/@type')
    publisher = xmlmap.StringField('mods:publisher')
    
class physicalDescription(_BaseMODS):
    '''MODS physicalDescription element'''
    ROOT_NAME = 'physicalDescription'
    extent = xmlmap.StringField("mods:extent")
    digital_origin = xmlmap.StringField("mods:digitalOrigin")


class subject(_BaseMODS):
    '''MODS subjec element with child mods:topic elements'''
    geographics = xmlmap.StringListField("mods:geographic")
    names = xmlmap.StringListField("mods:name")
    temporals = xmlmap.StringListField("mods:temporal")
    topics = xmlmap.StringListField("mods:topic")

class titleInfo(_BaseMODS):
    'MODS title element including titleInfo element'
    ROOT_NAME = 'titleInfo'
    sub_title = xmlmap.StringField("mods:subTitle",required=False)
    title = xmlmap.StringField("mods:title",required=True)

class typeOfResource(_BaseMODS):
    'MODS typeOfResource element'
    collection = xmlmap.StringField("@collection",
                                    choices=["yes"])
    manuscript = xmlmap.StringField("@manuscript",
                                    choices=["no"])

    

class MetadataObjectDescriptionSchema(_BaseMODS):
    """
    XmlObject for a single MODS record

    If no node is specified when initialized, a new, empty MODS
    XmlObject will be created.
    """    
    ROOT_NAME = 'mods'

    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)

    elements = xmlmap.NodeListField('mods:*', MODSElement)
    'list of all MODS elements as instances of :class:`MODSElement`'

    abstract = xmlmap.StringField('mods:abstract')
    genre = xmlmap.NodeField('mods:genre',genre)
    identifiers = xmlmap.NodeListField('mods:identifier',identifier)
    languages = xmlmap.NodeListField('mods:language',language)
    names = xmlmap.NodeListField('mods:name',name)
    notes = xmlmap.NodeListField('mods:note',note)
    origin_info = xmlmap.NodeField('mods:originInfo',originInfo)
    physical_description = xmlmap.NodeField('mods:physicalDescription',
                                            physicalDescription)
    subjects = xmlmap.NodeListField('mods:subject',subject)
    title_info = xmlmap.NodeField('mods:titleInfo',titleInfo)
    type_of_resource = xmlmap.NodeField('mods:typeOfResource',
                                        typeOfResource)
