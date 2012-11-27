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
#   AnalyzerMetadata
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class AnalyzerMetadata(AnalyzerFactory):
    """
    DESCRIPTION:
        
    PARAMETERS:
    """
    
    # description of analyzer
    description = "A metadata analyzer"
    
    # supported methods for validation
    available_methods = {   "dc"   :   "Dublin Core" }

    dependencies = {}
    
    css_report = "css/report.css"


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(path_info)
    # ==========================================================================
    def __init__(self, path_info, method):
        AnalyzerFactory.__init__(   self, 
                                    AnalyzerMetadata.description, 
                                    AnalyzerMetadata.available_methods, 
                                    AnalyzerMetadata.dependencies,
                                    path_info   )
        self.method = method
       

        # datastructures
        self.metadata_status = dict()
        self.metadata = None
        
        # path info
        self.metadata_reports_file = self.report_path + "/metadata.html"
        self.metadata_file =  self.working_path + "Metadata"



    # ==========================================================================
    # METHOD:
    #   analyze(self, filename)
    # ==========================================================================
    def analyze(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        parsable = "ok"
        
        # parsed metadata
        self.metadata = self.parser_runeberg.parse_metadata()

        # check if Metadata was parsed correctly
        all_none = True
        for metadata in self.metadata.keys():
            if self.metadata[metadata][0] is not None:
                all_none = False
        # could not parse Metadata 
        if all_none:
            parsable = "error"

        # check what validation method (dc, daisy, idpf)
        # search and open metadata
        must_missing = 0

        for key, value in self.metadata.iteritems():
            metadata_level = value[5]
            metadata_value = value[1]
            if metadata_level  is "must" and metadata_value is None:
                must_missing += 1


        # populate metadata status
        if must_missing == 0:
            status = "ok"
        else:
            status = "error"
        
        detailed_report = "metadata.html"

        self.metadata_status = { "must_missing"  :   must_missing,
                            "status"        :   status,
                            "parsable"      :       parsable,
                            "details"      :   detailed_report
                            }


        # build a detailed report
        self.build_detailed_report()

        return self.metadata_status



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
        level = None
        header = ["Metadata", "Type", "Value"]
        
        # build xhtml skeleton
        tree = self.xml_operations.build_xhtml_skel_final("Metadata", self.css_report)
        root = tree.getroot()

        # build table skeleton
        body = etree.Element("body")
        root.append(body)
        tbody = self.xml_operations.build_table_skel(body, "Metadata report", header)
        
        #
        # table entries
        #
        attrib = { "class" : "row"}
        for metadata in self.metadata.keys():
            tr = etree.Element("tr")
            tbody.append(tr)
            
            level = self.metadata[metadata][5]
            value = self.metadata[metadata][1]

            # location
            td = etree.Element("td", attrib)
            td.text = metadata
            tr.append(td)
            
            # type
            td = etree.Element("td", attrib)
            td.text = level
            tr.append(td)

            # message
            td = etree.Element("td", attrib)
            # use list values
            if isinstance(value, list):
                lookup_values = self.metadata[metadata][4]
                # use lookup strings
                if len(lookup_values) > 0:
                    value_str = ','.join(value)
                    lookup_str = ','.join(lookup_values)
                    values = value_str + "(lookup:" + lookup_str + ")"
                # use value keys
                else:
                    values = ''.join(value)
                td.text = values
            # use single value
            else:
                td.text = value

            tr.append(td)
            
        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)
        
        # write xml tree to file
        self.file_operations.write_unicode_final(self.metadata_reports_file, root_unicode)
    

    # ==========================================================================
    # METHOD:
    #   spellcheck(filename, markup_status)
    # ==========================================================================
    def spellcheck(self, filename, markup_status):
        pass
