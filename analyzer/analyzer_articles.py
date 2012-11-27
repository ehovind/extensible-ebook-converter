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

from lxml import etree as etree
from analyzer.analyzer_factory import AnalyzerFactory
# ==========================================================================
# CLASS:
#   AnalyzerArticles
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class AnalyzerArticles(AnalyzerFactory):
    """
    DESCRIPTION:
        
    PARAMETERS:
    """
    
    # description of analyzer
    description = "A metadata analyzer"
    
    # supported methods for validation
    available_methods = {   "Dublin Core"   :   "bla bla",
                            "Daisy"         :   "bla bla bla"   }

    dependencies = {}
    
    css_report = "css/report.css"


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(path_info)
    # ==========================================================================
    def __init__(self, path_info):
        AnalyzerFactory.__init__(   self, 
                                    AnalyzerArticles.description, 
                                    AnalyzerArticles.available_methods, 
                                    AnalyzerArticles.dependencies,
                                    path_info   )
        
        # datastructures
        self.articles_status = dict()
        self.articles = None

        # path info
        self.articles_file =  self.working_path + "Metadata"
        self.articles_reports_file = self.report_path + "/articles.html"
        


    # ==========================================================================
    # METHOD:
    #   analyze(filename)
    # ==========================================================================
    def analyze(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        detailed_report = "articles.html"
        
        # parsed articles
        self.articles = self.parser_runeberg.parse_articles_lst()

        status = "ok"
        part_missing = 0
        parsable = "ok"

        self.articles_status = { "part_missing"  :   part_missing,
                            "status"        :   status,
                            "parsable"      :       parsable,
                            "details"      :   detailed_report
                            }


        # build a detailed report
        self.build_detailed_report()

        return self.articles_status






        


    # ==========================================================================
    # METHOD:
    #   build_detailed_report()
    # ==========================================================================
    def build_detailed_report(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        header = ["Part", "Filename"]
        
        # build xhtml skeleton
        tree = self.xml_operations.build_xhtml_skel_final("Articles", self.css_report)
        root = tree.getroot()

        # build table skeleton
        body = etree.Element("body")
        root.append(body)
        tbody = self.xml_operations.build_table_skel(body, "Articles report", header)
        
        #
        # table entries
        #
        attrib = { "class" : "row"}
        for article in self.articles:
            tr = etree.Element("tr")
            tbody.append(tr)
            
            part = article[0]
            filename = article[1]

            # part
            th = etree.Element("th", attrib)
            th.text = part
            tr.append(th)
            
            # filename
            th = etree.Element("th", attrib)
            th.text = filename
            tr.append(th)


        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)
        
        # write xml tree to file
        self.file_operations.write_unicode_final(self.articles_reports_file, root_unicode)
    
    # ==========================================================================
    # METHOD:
    #   spellcheck(filename, markup_status)
    # ==========================================================================
    def spellcheck(self, filename, markup_status):
        pass
