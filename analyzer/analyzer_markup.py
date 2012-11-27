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

import os
import sys
from lxml import etree
from lxml import html
import tidy

from analyzer.analyzer_factory import AnalyzerFactory
from . import analyzer_unicode as AnalyzerUnicode
# ==========================================================================
# CLASS:
#   Fetcher
#
# CONSTRUCTOR:
#   workspace
#   valid_domains
#   args
#
# CLASS VARIABLES:
#   None
#
# DESCRIPTION:
# ==========================================================================
class AnalyzerMarkup(AnalyzerFactory):
    """
    DESCRIPTION:
        
    PARAMETERS:
    """
    
    # description of validator
    description = "A markup validator"
    
    # supported methods for validation
    available_methods = {   "tidy": "validate and correctHTML files",
                            "lxml": " library for processing XML and HTML"}

    dependencies = {    "lxml"  :   "library",
                        "tidy"  :   "library"   }
    

    xhtml_validator = "-//W3C//DTD XHTML 1.1//EN"

    css_report = "../css/report.css"


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(path_info, method)
    # ==========================================================================
    def __init__(self, path_info, method):
        AnalyzerFactory.__init__(self, AnalyzerMarkup.description, 
                                 AnalyzerMarkup.available_methods, 
                                 AnalyzerMarkup.dependencies,
                                 path_info)
        self.method = method
        
        # datastructures
        self.markup_status = list()

        # path info
        self.markup_reports_path = self.report_path + "/markup/"

    # ==========================================================================
    # METHOD:
    #   analyze(filename, encoding)
    # ==========================================================================
    def analyze(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        first = True

        # 
        # analyze using lxml
        #
        if self.method == "lxml":
            # display debug info
            if first:
                #print "\tusing: " +self.method + "...",
                pass
           
            # analyze using lxml
            errors = self.analyze_lxml(filename)

            # check if validator failed
            if len(errors) > 0:
                if errors[0] == "disabled" and first:
                    print "could not validate non-XHTML document"
            
            first = False
        #
        # analyze using tidy
        #   
        if self.method == "tidy":
            if first:
                #print "\tusing: " +self.method
                first = False
            errors = self.analyze_tidy(filename)
      
        # populate markup_status
        if len(errors) == 0:
            status = "ok"
            detailed_report = None
        else:
            status = "error"
            filename_only = self.file_operations.filename_only_final(filename)
            detailed_report = "markup/" + filename_only

        # populate markup_status
        self.markup_status = {  "title"     : "Markup validator",
                                "errors"    :   errors,
                                "status"    :   status,
                                "details"  :   detailed_report}
        # build a detailed report
        if len(self.markup_status["errors"]) > 0:
            self.build_detailed_report(filename)
        

        return self.markup_status

            

    # ==========================================================================
    # METHOD:
    #   analyze_lxml(filename)
    # ==========================================================================
    def analyze_lxml(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        
        errors = list()

        try:
            dtd = etree.DTD(external_id = AnalyzerMarkup.xhtml_validator)

            # parse and the XHTML
            parser = html.XHTMLParser()
            tree = etree.parse(filename, parser)

            # validate tree
            dtd.validate(tree)

            # get a list of error messages 
            errors = dtd.error_log.filter_from_errors()
        except etree.XMLSyntaxError as err:
            errors = ["Failed parsing XHTML, check well-formed tags:"+ str(err)]

        # return list of errors
        return errors
        
        

    # ==========================================================================
    # METHOD:
    #   analyze_tidy(filename, encoding)
    # ==========================================================================
    def analyze_tidy(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        encoding_tidy = None
        
        try:
            analyzer_unicode = AnalyzerUnicode.AnalyzerUnicode(self.path_info, "file")
            encoding = analyzer_unicode.analyze(filename)["encoding"]
        except NotImplementedError:
            print "[FATAL] Analyzer not implemented"
            sys.exit(1)

        # set file encoding to prevent false positives
        if encoding == "utf-8":
            encoding_tidy = encoding.replace("-","")
        if encoding == "iso-8859-1":
            encoding_tidy = "latin1"
        if encoding == "us-ascii":
            encoding_tidy = "latin1"
        options = {"input-encoding" : encoding_tidy}
        
        try:
            document = tidy.parse(filename, **options)
            #document, error = tidy_document(open(filename).read(), options)

        except tidy.TidyLibError as err: 
            print "could not read file content, check encoding:",
            print os.path.basename(filename),
            print err
            sys.exit(1)
        
        return document.get_errors()


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
        location = None
        level = None
        message = None
        header = ["Location", "Type", "Message"]
        
        # build xhtml skeleton
        tree = self.xml_operations.build_xhtml_skel_final(filename, self.css_report)
        root = tree.getroot()

        # build table skeleton
        body = etree.Element("body")
        root.append(body)
        tbody = self.xml_operations.build_table_skel(body, "Spellcheck report", header)
        
        #
        # table entries
        #
        attrib = { "class" : "row"}
        
        # add all errors
        for error in self.markup_status["errors"]:
            tr = etree.Element("tr")
            tbody.append(tr)
            
            # parse tidy error message
            if self.method == "tidy":
                error_message = str(error)
                location = error_message.split("-")[0]
                level = (error_message.split("-")[1]).split(":")[0]
                message = error_message.split(":")[1].decode('utf8')
            else:
                # error log is written
                if isinstance (error, etree._LogEntry):
                    location = str(error.line)
                    level = error.level_name
                    message = error.message
                # could not parse document at all
                else:
                    message = error

            # location
            th = etree.Element("th", attrib)
            th.text = location
            tr.append(th)
            
            # type
            th = etree.Element("th", attrib)
            th.text = level
            tr.append(th)

            # message
            th = etree.Element("th", attrib)
            th.text = message
            tr.append(th)

        
            # serialize the XML to Unicode strings
            root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)

            # write xml tree to file
            if not os.path.exists(self.markup_reports_path):
                os.mkdir(self.markup_reports_path)

            filename_only = self.file_operations.filename_only_final(filename)
            report_file = self.markup_reports_path + filename_only
            self.file_operations.write_unicode_final(report_file, root_unicode)
    
    # ==========================================================================
    # METHOD:
    #   spellcheck(filename, markup_status)
    # ==========================================================================
    def spellcheck(self, filename, markup_status):
        pass
    
    
    


