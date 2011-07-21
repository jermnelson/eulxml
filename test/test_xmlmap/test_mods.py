# file test_xmlmap/test_mods.py
# 
#   Copyright 2011 Colorado College
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

#!/usr/bin/env python

import unittest
from os import path

from eulxml.xmlmap  import load_xmlobject_from_file, load_xmlobject_from_string
from eulxml.xmlmap import mods
from testcore import main

class TestMods(unittest.TestCase):
    FIXTURE_FILE = path.join(path.dirname(path.abspath(__file__)) ,
                             'fixtures', 'thesis_mods.xml')
    def setUp(self):
        self.mods = load_xmlobject_from_file(self.FIXTURE_FILE, 
                                             mods.MetadataObjectDescriptionSchema)

    def test_init(self):
        self.assert_(isinstance(self.mods,
                                mods.MetadataObjectDescriptionSchema))

    def test_basic_fields(self):
        self.assertEqual(unicode(self.mods.abstract.value), 
                         u'''The efficient market hypothesis fails to fully explain market behavior.  Behavioral economics is a new field that contributes insights to stock market analysis.  Throughout history there have been many panics and crashes, with the most recent one being the 2008 housing bubble.  This thesis seeks to find evidence and explain, through behavioral economic theory, why investors panic and behave irrationally to bad news.  It will utilize the asymmetric utility function along with other behavioral economic theory to find evidence through the market reaction to good quarterly earnings reports and bad quarterly earnings reports.  This thesis hopes to show that good news and bad news of equal magnitude result in different reactions in the stock market, as measured through share price and trading volume.''')

    def test_validation(self):
        self.assertTrue(self.mods.schema_valid())

    def test_genre(self):
        self.assertEquals('marcgt',self.mods.genre.authority)
        self.assertEquals('thesis',self.mods.genre.value)
    

    def test_language(self):
        self.assert_(isinstance(self.mods.languages[0],
                                mods.language))
        english = self.mods.languages[0]
        self.assertEquals('eng',
                          english.terms[0].value)

    def test_names(self):
        student_author = self.mods.names[0]
        self.assert_(isinstance(student_author,
                                mods.name))
        
        self.assertEquals('Wildnauer-Haigney, Kyle',
                          student_author.name_parts[0].value)
        self.assertEquals('personal',
                          student_author.type)
        self.assertEquals('text',
                          student_author.roles[0].role_term.type)
        self.assertEquals('marcrelator',
                          student_author.roles[0].role_term.authority)
        self.assertEquals('creator',
                          student_author.roles[0].role_term.value)
        advisor = self.mods.names[1]
        self.assert_(isinstance(advisor,mods.name))
        self.assertEquals('Smith, Mark',advisor.name_parts[0].value)
        self.assertEquals('personal',advisor.type)
        self.assertEquals('text',advisor.roles[0].role_term.type)
        self.assertEquals('marcrelator',
                          advisor.roles[0].role_term.authority)
        self.assertEquals('thesis advisor',
                          advisor.roles[0].role_term.value)
        department = self.mods.names[2]
        self.assert_(isinstance(department,mods.name))
        self.assertEquals('Department of Economics and Business',
                          department.name_parts[0].value)
        self.assertEquals('corporate',department.type)
        self.assertEquals('text',department.roles[0].role_term.type)
        self.assertEquals('marcrelator',
                          department.roles[0].role_term.authority)
        self.assertEquals('sponsor',
                          department.roles[0].role_term.value)
        institution = self.mods.names[3]
        self.assert_(isinstance(institution,mods.name))
        self.assertEquals('Colorado College',
                          institution.name_parts[0].value)
        self.assertEquals('corporate',institution.type)
        self.assertEquals('text',institution.roles[0].role_term.type)
        self.assertEquals('marcrelator',
                          institution.roles[0].role_term.authority)
        self.assertEquals('degree grantor',
                          institution.roles[0].role_term.value)


    def test_notes(self):
        degree_type = self.mods.notes[0]
        self.assert_(isinstance(degree_type,mods.note))
        self.assertEquals('Degree Type',degree_type.display_label)
        self.assertEquals('thesis',degree_type.type)
        self.assertEquals('bachelor',degree_type.value)
        degree_name = self.mods.notes[1]
        self.assert_(isinstance(degree_name,mods.note))
        self.assertEquals('Degree Name',degree_name.display_label)
        self.assertEquals('thesis',degree_name.type)
        self.assertEquals('Bachelor of Arts',degree_name.value)
        thesis_note = self.mods.notes[2]
        self.assert_(isinstance(thesis_note,mods.note))
        self.assertEquals('thesis',thesis_note.type)
        self.assertEquals('Senior Thesis -- Colorado College',
                          thesis_note.value)
        bib_note = self.mods.notes[3]
        self.assert_(isinstance(bib_note,mods.note))
        self.assertEquals('bibliography',bib_note.type)
        self.assertEquals('Includes bibliographical references',
                          bib_note.value)

        


    def test_originInfo(self):
        origin_info = self.mods.origin_info
        self.assert_(isinstance(origin_info,mods.originInfo))
        self.assertEquals('text',
                          origin_info.place_term_type)
        self.assertEquals('Colorado Springs, Colo',
                          origin_info.place_term)
        self.assertEquals('Colorado College',
                          origin_info.publisher)
        self.assertEquals('2011',origin_info.date_captured)
        self.assertEquals('2011',origin_info.date_issued)
        self.assertEquals('yes',origin_info.date_issued_keydate)


    def test_physicalDescription(self):
        phy_desc = self.mods.physical_description
        self.assert_(isinstance(phy_desc,
                                mods.physicalDescription))
        self.assertEquals('51 p. : ill.',
                          phy_desc.extent)
        self.assertEquals('born digital',phy_desc.digital_origin)

    def test_subjects(self):
        subject_one = self.mods.subjects[0]
        self.assertEquals('Behavioral Economics',
                          subject_one.topics[0])
        subject_two =  self.mods.subjects[1]
        self.assertEquals('Asymmetric Utility Function',
                          subject_two.topics[0])
        subject_three = self.mods.subjects[2]
        self.assertEquals('Earnings Reports',
                          subject_three.topics[0])
  

    def test_titleInfo(self):
        self.assert_(isinstance(self.mods.title_info, 
                                mods.titleInfo))
        titleInfo = self.mods.title_info
        self.assertEqual('Asymmetric Behavior in the Stock Market',
                         titleInfo.title) 

class TestCreateMods(unittest.TestCase):
    ''' `TestCreateMods` tests runtime creation of a simple MODS
       thesis object.
    '''
    def setUp(self):
        self.mods = mods.MetadataObjectDescriptionSchema()
        self.abstract_txt = u'''The value and importance of diversity in one's 
portfolio has long been postulated, but it
was Harry M. Markowitz who proposed the first mathematical model that would allow
investors to systematically compute the optimal allocation of assets based on individual
preferences (the investor's utility function), covariance, variance, and expected value of
returns. Adequate diversification can mitigate risk substantially while potentially
enhancing returns. Markowitz provided investors with the tools to optimally diversify
their investments.'''
        self.mods.abstract = mods.abstract(value=self.abstract_txt)
        creator = mods.name(type="personal",
                            display_form="Sargent, Blair M.")
        creator_role = mods.role(role_term=mods.roleTerm(authority='marcrt',
                                                         type='text',
                                                         value='creator'))
        creator.roles.append(creator_role)
        creator.name_parts.append(mods.namePart(type="given",value='Blair'))
        creator.name_parts.append(mods.namePart(type="middle",value="M"))
        creator.name_parts.append(mods.namePart(type="family",value="Sargent"))
        self.mods.names.append(creator)
        advisor = mods.name(type="personal")
        advisor.name_parts.append(mods.namePart(value="de Arauju, Pedro"))
        advisor_role = mods.role(role_term=mods.roleTerm(authority='marcrt',
                                                         type='text',
                                                         value='advisor'))
        advisor.roles.append(advisor_role)
        self.mods.names.append(advisor)
        department = mods.name(type='corporate')
        department.name_parts.append(mods.namePart(value='Department of Economics and Business'))
        department.roles.append(mods.role(role_term=mods.roleTerm(authority='marcrt',
                                                                  type='text',
                                                                  value='sponsor')))
        self.mods.names.append(department)
        institution = mods.name(type='corporate')
        institution.name_parts.append(mods.namePart(value='Colorado College'))
        institution.roles.append(mods.role(role_term=mods.roleTerm(authority='marcrt',
                                                                   type='text',
                                                                   value='degree grantor')))
        self.mods.names.append(institution)
        self.mods.genre = mods.genre(authority='marcgt',
                                     value='thesis')
        pid = mods.identifier(type='pid',
                              value='coccc:3156')
        self.mods.identifiers.append(pid)
        english = mods.languageTerm(type='code',
                                    value='EN')
        eng_language = mods.language(terms=[english,])
        self.mods.languages.append(eng_language)
        self.thesis_note = mods.note(type='thesis',
                                     value='Senior Thesis -- Colorado College')
        self.mods.notes.append(self.thesis_note)
        self.origin_info = mods.originInfo(date_captured='2011',
                                           date_issued='2011',
                                           date_issued_keydate='yes',
                                           place_term='Colorado Springs, Colo.',
                                           place_term_type='text',
                                           publisher='Colorado College')
        self.mods.origin_info = self.origin_info
        self.mods.physical_description = mods.physicalDescription(extent='56 p. ill.',
                                                                  digital_origin='born digital')
        self.mods.type_of_resource  = mods.typeOfResource(value="text")
        self.mods.title_info = mods.titleInfo()
        self.mods.title_info.title = 'Security Return Covariance Forecasting ' +\
                                     'and Applications for Multi-Period ' +\
                                     'Mean-Variance Formulation'
       
        
    def test_abstract(self):
        self.assert_(isinstance(self.mods.abstract,
                                mods.abstract))
        self.assertEqual(self.mods.abstract.value,
                         self.abstract_txt)

    def test_advisor(self):
        advisor = self.mods.names[1]
        self.assert_(isinstance(advisor,
                                mods.name))
        self.assert_(isinstance(advisor.name_parts[0],
                                mods.namePart))
        self.assert_(isinstance(advisor.roles[0],
                                mods.role))
        self.assert_(isinstance(advisor.roles[0].role_term,
                                mods.roleTerm))
        self.assertEquals('personal',
                          advisor.type)
        self.assertEquals('de Arauju, Pedro',
                          advisor.name_parts[0].value)
        self.assertEquals('marcrt',
                          advisor.roles[0].role_term.authority)
        self.assertEquals('text',
                          advisor.roles[0].role_term.type)
        self.assertEquals('advisor',
                          advisor.roles[0].role_term.value)




    def test_creator(self):
        creator = self.mods.names[0]
        self.assert_(isinstance(creator,
                                mods.name))
        self.assert_(isinstance(creator.name_parts[0],
                                mods.namePart))
        self.assertEquals('personal',
                          creator.type)
        self.assertEquals("Sargent, Blair M.",
                          creator.display_form)
        self.assertEquals(creator.name_parts[0].value,
                          "Blair")
        self.assertEquals(creator.name_parts[0].type,
                          "given")
        self.assertEquals(creator.name_parts[1].value,
                          "M")
        self.assertEquals(creator.name_parts[1].type,
                          "middle")
        self.assertEquals(creator.name_parts[2].value,
                          "Sargent")
        self.assertEquals(creator.name_parts[2].type,
                          "family")
        self.assertEquals(creator.roles[0].role_term.value,
                          "creator")
        self.assertEquals(creator.roles[0].role_term.type,
                          "text")
        self.assertEquals(creator.roles[0].role_term.authority,
                          "marcrt")

    def test_department(self):
        department = self.mods.names[2]
        self.assert_(isinstance(department,
                                mods.name))
        self.assert_(isinstance(department.name_parts[0],
                                mods.namePart))
        self.assert_(isinstance(department.roles[0],
                                mods.role))
        self.assert_(isinstance(department.roles[0].role_term,
                                mods.roleTerm))
        self.assertEquals(department.type,'corporate')
        self.assertEquals(department.name_parts[0].value,
                          'Department of Economics and Business')
        self.assertEquals(department.roles[0].role_term.value,
                          "sponsor")
        self.assertEquals(department.roles[0].role_term.type,
                          "text")
        self.assertEquals(department.roles[0].role_term.authority,
                          "marcrt")



    def test_genre(self):
        self.assertEquals('marcgt',self.mods.genre.authority)
        self.assertEquals('thesis',self.mods.genre.value)

    def test_identifiers(self):
        pid_id = self.mods.identifiers[0]
        self.assertEqual('pid',
                         pid_id.type)
        self.assertEqual('coccc:3156',
                         pid_id.value)

    def test_institution(self):
        institution = self.mods.names[3]
        self.assert_(isinstance(institution,
                                mods.name))
        self.assert_(isinstance(institution.name_parts[0],
                                mods.namePart))
        self.assert_(isinstance(institution.roles[0],
                                mods.role))
        self.assert_(isinstance(institution.roles[0].role_term,
                                mods.roleTerm))
        self.assertEquals(institution.type,'corporate')
        self.assertEquals(institution.name_parts[0].value,
                          'Colorado College')
        self.assertEquals(institution.roles[0].role_term.value,
                          "degree grantor")
        self.assertEquals(institution.roles[0].role_term.type,
                          "text")
        self.assertEquals(institution.roles[0].role_term.authority,
                          "marcrt")
                        
    def test_languages(self):
        english = self.mods.languages[0]
        self.assertEqual('code',
                         english.terms[0].type)
        self.assertEqual('EN',
                         english.terms[0].value)

    def test_notes(self):
        for note in self.mods.notes:
            self.assert_(isinstance(note,
                                    mods.note))
        self.assertEquals(self.mods.notes[0].value,
                          self.thesis_note.value)
    
    def test_originInfo(self):
        print("Origin info type=%s" % self.origin_info.place_term)
        self.assert_(isinstance(self.mods.origin_info,
                                mods.originInfo))
        self.assertEquals('text',
                          self.mods.origin_info.place_term_type)
        self.assertEquals('Colorado Springs, Colo.',
                          self.mods.origin_info.place_term)
        self.assertEquals('Colorado College',
                          self.mods.origin_info.publisher)


    def test_physicalDescription(self):
        self.assert_(isinstance(self.mods.physical_description,
                                mods.physicalDescription))
        self.assertEquals('56 p. ill.',
                          self.mods.physical_description.extent)
        self.assertEquals('born digital',
                          self.mods.physical_description.digital_origin)

    def test_titleInfo(self):
        self.assert_(isinstance(self.mods.title_info, 
                                mods.titleInfo))
        titleInfo = self.mods.title_info
        self.assertEqual(titleInfo.title,
                         'Security Return Covariance Forecasting ' +\
                         'and Applications for Multi-Period ' +\
                         'Mean-Variance Formulation')

    def test_typeOfResource(self):
        self.assert_(isinstance(self.mods.type_of_resource,
                                mods.typeOfResource))
        self.assertEquals('text',
                          self.mods.type_of_resource.value)
        



if __name__ == '__main__':
    main() 
