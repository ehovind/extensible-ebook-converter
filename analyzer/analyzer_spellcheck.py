"""
This file is part of Extensible eBook Converter (EeCon),
an advanced ebook analysis and conversion tool.
Copyright (C) 2012 Espen Hovind <espehov@ifi.uio.no>

EeCon is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Eeon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EeCon.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
from enchant.checker import SpellChecker
from enchant import DictNotFoundError
from lxml import etree
from analyzer.analyzer_factory import AnalyzerFactory
import StringIO

# ==========================================================================
# CLASS:
#   AnalyzerSpellcheck
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class AnalyzerSpellcheck(AnalyzerFactory):
    """
    DESCRIPTION:
        
    PARAMETERS:
    """
    
    # description of analyzer
    description = "A spellcheck analyzer"
    
    # supported methods for validation
    available_methods = {"aspell":"Aspell" }

    dependencies = {    "aspell"    :   "external",
                        "enchant"   :   "library"    }
    

    css_report = "../css/report.css"


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(path_info, method)
    # ==========================================================================
    def __init__(self, path_info, method):
        AnalyzerFactory.__init__(   self, 
                                    self.description, 
                                    self.available_methods, 
                                    self.dependencies,
                                    path_info   )
        self.method = method
        self.language = None

        # datastructures
        self.spelling_status = list()

        # path information
        self.spellcheck_reports_path = self.report_path + "/spellcheck/"


    # ==========================================================================
    # METHOD:
    #   spellcheck(filename, markup_status)
    # ==========================================================================
    def spellcheck(self, filename, markup_status):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        typo = None
        report = list()
        supported = True


        if self.language is None:
            print "[ERROR] unknown language, specify with --language"
            sys.exit(1)

        # set prefered spellcheck method
        #b = Broker()
        #b.set_ordering("nb","myspell,aspell")

        # create a SpellChecker based on book's language
        try:
            checker = SpellChecker(self.language)  
        except DictNotFoundError as err:
            print "language not supported by installed dictionaries"
            supported = False
            

        print "(lang: " +self.language +")"
        
       
        # check if document is valid XHTML
        if len(markup_status["errors"]) > 0 or not supported:
            invalid = "N/A"
            self.spelling_status = {  "title"     : "Spellcheck",
                                "errors"    :   list(),
                                "status"    :   invalid,
                                "details"  :   None}

            return self.spelling_status

        # get a list of words
        parser = etree.XMLParser()
        xhtml = self.file_operations.read_xml_final(filename)
        tree = etree.parse(StringIO.StringIO(xhtml), parser)
        root = tree.getroot()

        # extract plain text
        words = root.xpath("//text()")

        # convert to text
        text = ''.join(words)

        # perform a spellcheck using chosen tool
        try:

            # set text to check
            checker.set_text(text)
        
            for err in checker:
                typo = err.word
                report.append(typo)   

            
            # make list distinct
            report_dist = list(set(report))
            report_sorted = sorted(report_dist)

            # add to report
            if len(report_sorted) == 0:
                status = "ok"
                detailed_report = None
            else:
                status = "error"
                filename_only = self.file_operations.filename_only_final(filename)
                detailed_report = "spellcheck/" + filename_only

            self.spelling_status = {  "title"     : "Spellcheck",
                                "errors"    :   report_sorted,
                                "status"    :   status,
                                "details"  :   detailed_report}

            if len(self.spelling_status["errors"]) > 0:
                self.build_detailed_report(filename)

        except IOError as err:
            print err
        

        #print "done."
        return self.spelling_status

    # ==========================================================================
    # METHOD:
    #   set_language(language)
    # ==========================================================================
    def set_language(self, language):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        self.language = language
        

    # ==========================================================================
    # METHOD:
    #   build_detailed_report(filename)
    # ==========================================================================
    def build_detailed_report(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        
        # build xhtml skeleton
        tree = self.xml_operations.build_xhtml_skel_final(filename, self.css_report)
        root = tree.getroot()

        # build table skeleton
        body = etree.Element("body")
        root.append(body)
        header = ["Word"]
        tbody = self.xml_operations.build_table_skel(body, "Spellcheck report", header)
        
        #
        # table entries
        #
        attrib = { "class" : "row"}
        
        for word in self.spelling_status["errors"]:
            tag_tr = etree.Element("tr")
            tbody.append(tag_tr)
            
            tag_td = etree.Element("td", attrib)
            tag_td.text = word
            tag_tr.append(tag_td)


        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)

        # write xml tree to file
        if not os.path.exists(self.spellcheck_reports_path):
            os.mkdir(self.spellcheck_reports_path)

        filename_only = self.file_operations.filename_only_final(filename)
        report_file = self.spellcheck_reports_path + filename_only
        self.file_operations.write_unicode_final(report_file, root_unicode)


    # ==========================================================================
    # METHOD:
    #   analyze(filename, encoding)
    # ==========================================================================
    def analyze(self, filename):
        pass
