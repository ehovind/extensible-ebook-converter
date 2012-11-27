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
import shutil
from lxml import etree as etree

from analyzer.analyzer_unicode import AnalyzerUnicode
from analyzer.analyzer_markup import AnalyzerMarkup
from analyzer.analyzer_spellcheck import AnalyzerSpellcheck
from analyzer.analyzer_metadata import AnalyzerMetadata
from analyzer.analyzer_articles import AnalyzerArticles
from analyzer.report_entry import ReportEntry
from converter import parser_runeberg as ParserRuneberg
from shared import file_operations as FileOperations
from shared import xml_operations as XMLOperations
# ==========================================================================
# CLASS:
#   SourceAnalyzer
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class SourceAnalyzer(object):
    """
    DESCRIPTION:
        
    PARAMETERS:
    """
   

    css_report_template = "analyzer/resources/report.css"
    cover_gif = "cover.gif"

    # css file relative to report dir path
    css_link_file = "css/report.css"


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(workspace, args)
    # ==========================================================================
    def __init__(self, workspace, args):
        self.workspace = workspace
        self.args = args
       
        # parsed arguments
        self.title = None
        self.language = None
        self.encoding_method = "file"
        self.markup_method = "tidy"
        self.metadata_method = "dc"
        self.spellcheck_method = "aspell"

        # workspace path info
        self.path_info = dict()
        
        # external classes
        self.file_operations = FileOperations.FileOperations()
        self.xml_operations = XMLOperations.XMLOperations()
        self.parser_runeberg = None
            
        # parsed metadata
        self.metadata = None


    
    # ==========================================================================
    # METHOD:
    #   process()
    # ==========================================================================
    def process(self):
        """
        DESCRIPTION:
            Process the command line arguments and initalize the analyzers.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """

        # parse command line arguments into variables
        self.parse_config()
        
        # prepare workspace path information
        self.path_info = self.prepare_path_info(self.title)
        
        # init local path variables
        books_path = self.path_info["books_path"]
        working_path = self.path_info["working_path"]
        report_path = self.path_info["report_path"]
        articles_file = self.path_info["articles_file"]
        metadata_file = self.path_info["metadata_file"]


        # check if title is fetched
        if not self.check_title_exists():
            print "[FATAL] this title is not fetched. ",
            print "Available titles: ", os.listdir(books_path)
            sys.exit(1)
        
        # Initialize the analyzers
        analyzer_unicode = AnalyzerUnicode(self.path_info, self.encoding_method)
        analyzer_unicode.check_dependencies("Encoding analyzer")
        analyzer_metadata = AnalyzerMetadata(self.path_info, self.metadata_method)
        analyzer_metadata.check_dependencies("Metadata analyzer")
        analyzer_articles = AnalyzerArticles(self.path_info)
        analyzer_articles.check_dependencies("Article analyzer")
        analyzer_markup = AnalyzerMarkup(self.path_info, self.markup_method)
        analyzer_markup.check_dependencies("Markup analyzer")
        analyzer_spellcheck = AnalyzerSpellcheck(self.path_info, self.spellcheck_method)
        analyzer_spellcheck.check_dependencies("Spellcheck analyzer")
        
        # check encoding status
        if not analyzer_unicode.validate_encoding():
            print "[ERROR] non utf-8 encoding detected, check with eanalyze.py"
            print "[ERROR] Suggestion: convert manually with iconv"
            sys.exit(1)

        # prepare the workspace report structure
        if not os.path.exists(report_path):
            self.prepare_workspace_folders()
        
            
       
        # 
        # analyze structure and meta
        #
        report_entries_structure = list()
        
        # articles
        try:
            report_entry = ReportEntry("articles", articles_file)
            file_encoding = analyzer_unicode.analyze(articles_file)
            report_entry.set_encoding(file_encoding)
            articles_status =  analyzer_articles.analyze(articles_file)
            report_entry.set_articles_status(articles_status)
            report_entries_structure.append(report_entry)
        except NotImplementedError:
            print "[FATAL] Analyzer not implemented"
            sys.exit(1)
        
        # metadata
        try:
            report_entry = ReportEntry("metadata", metadata_file)
            file_encoding = analyzer_unicode.analyze(metadata_file)
            report_entry.set_encoding(file_encoding)
            metadata_status =  analyzer_metadata.analyze(metadata_file)
            report_entry.set_metadata_status(metadata_status)
            report_entries_structure.append(report_entry)
        except NotImplementedError:
            print "[FATAL] Analyzer not implemented"
            sys.exit(1)


        
        #
        # set spellcheck language
        #
        self.parser_runeberg = ParserRuneberg.ParserRuneberg(None, self.path_info)
        self.metadata = self.parser_runeberg.parse_metadata()
        if self.language is None:
            if self.metadata["language"][1] is not None:
                self.language = self.metadata["language"][1]
            else:
                print "[ERROR] language not deteced, specify with --language"
                sys.exit(1)
        analyzer_spellcheck.set_language(self.language)
        
        content_files = self.file_operations.list_files(working_path, "*.html")
        report_entries_content = list()
        first = True
        for filename in content_files:
            print "\t[STATUS] processing file ", os.path.basename(filename),
            # initiate a new Report entry
            report_entry = ReportEntry("content", filename)

            # analyze file encoding 
            if first:
                pass
                #print "[STATUS] Analyze file encoding..."
            try:
                file_encoding = analyzer_unicode.analyze(filename)
                report_entry.set_encoding(file_encoding)

                # analyze markup
                if first:
                    pass
                    #print "[STATUS] Analyze markup..."
                markup_status =  analyzer_markup.analyze(filename)
                report_entry.set_markup_status(markup_status)
                
                # analyze spelling
                if first:
                    pass
                    #print "[STATUS] Perform spellchecking..."
                spellcheck_status =  analyzer_spellcheck.spellcheck(filename, markup_status)
                report_entry.set_spellcheck_status(spellcheck_status)
            except NotImplementedError:
                print "[FATAL] Analyzers not implemented"
                sys.exit(1)
            
            # add to list of report entries
            report_entries_content.append(report_entry)
            first = False




        # build a report summary
        self.build_report(report_entries_structure, report_entries_content)
       

        # display analyzer summary
        self.display_summary()
      


    # ==========================================================================
    # METHOD:
    #   parse_config()
    # ==========================================================================
    def parse_config(self):
        """
        DESCRIPTION:
            Parse command line arguments into path_info.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
   
        if "language" in self.args:
            if self.args['language'] is not None:
                self.language = self.args['language']
        
        if "markup" in self.args:
            if self.args['markup'] is not None:
                self.markup_method = self.args['markup']

        if "encoding" in self.args:
            if self.args['encoding'] is not None:
                self.encoding_method = self.args['encoding']

        if "metadata" in self.args:
            if self.args['metadata'] is not None:
                self.metadata_method = self.args['metadata']

        if "spellcheck" in self.args:
            if self.args['spellcheck'] is not None:
                self.spellcheck_method = self.args['spellcheck']

        # set publication title
        if "title" in self.args:
            if self.args['title'] is None:
                print "[ERROR] define a title with --title TITLE"
                sys.exit(1)

            self.title = self.args["title"]
            



    
    # ==========================================================================
    # METHOD:
    #   prepare_workspace_path_info()
    # ==========================================================================
    def prepare_path_info(self, title):
        """
        DESCRIPTION:
            Construct path info.
            
        PARAMETERS:
            None
        
        RETURN: 
            path_info   dict    Path information.
        """
        
        books_path  = self.workspace + "/books/"
        working_path = books_path + title + "/input/working_directory/"
        report_path = books_path + title + "/output/reports/"
        
        path_info = {   
            "books_path"    : self.workspace + "/books/", 
            "info_path"     : self.workspace + "/info/",
            "archive_path"  : books_path + title + "/input/archive/",
            "original_path" : books_path + title + "/input/original/",
            "working_path"  : books_path + title + "/input/working_directory/",
            "output_path"   : None,
            "report_path"   : report_path,
            "report_file"   : report_path + "/index.html",
            "report_css_path" : report_path + "/css/",
            "report_css_file" : report_path + "/css/report.css",
            "cover_file"    : working_path + "/images/" + self.cover_gif,
            "articles_file" : working_path + "Articles.lst",
            "metadata_file" : working_path + "Metadata"
        }
                        
        return path_info

    # ==========================================================================
    # METHOD:
    #   prepare_workspace_folders()
    # ==========================================================================
    def prepare_workspace_folders(self):
        """
        DESCRIPTION:
            Create folders in workspace. Copy report template.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
    
        report_path = self.path_info["report_path"]
        report_css_path = self.path_info["report_css_path"]
        report_css_file = self.path_info["report_css_file"]

        if not os.path.exists(report_path):
            os.makedirs(report_path)
        
        if not os.path.exists(report_css_path):
            os.makedirs(report_css_path)


        # copy style template
        shutil.copy2(self.css_report_template, report_css_file)


    
    # ==========================================================================
    # METHOD:
    #   build_report(report_entries_structure, report_entries_content)
    # ==========================================================================
    def build_report(self, report_entries_structure, report_entries_content):
        """
        DESCRIPTION:
            Build summary report.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        report_file = self.path_info["report_file"]
        # 
        
        # build the skeleton
        tree = self.xml_operations.build_xhtml_skel_final("Rapport", self.css_link_file)
        root = tree.getroot()
        body = etree.Element("body")
        root.append(body)

        # build table for Articles.lst and Metadata and insert rows
        header = ["Filename", "Encoding", "Parsable", "Status" ]
        table_name = "Publication structure and metadata"
        self.xml_operations.build_table_final_objects(body, table_name, header, report_entries_structure)
        
        # build table for publication content and insert rows
        header = ["Filename", "Encoding", "Markup", "Spellcheck"]
        table_name = "Publication content"
        self.xml_operations.build_table_final_objects(body, table_name, header, report_entries_content)

        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)
        
        # write xml tree to file
        self.file_operations.write_unicode_final(report_file, root_unicode)


    # ==========================================================================
    # METHOD:
    #   check_title_exists()
    # ==========================================================================
    def check_title_exists(self):
        """
        DESCRIPTION:
            Check if title is present in working directory.
            
        PARAMETERS:
            None
        
        RETURN: 
            exists  boolean     True if title exists, False if not.
        """
        if os.path.exists(self.path_info["working_path"]):
            return True
        else:
            return False

    # ==========================================================================
    # METHOD:
    #   display_summary()
    # ==========================================================================
    def display_summary(self):
        """
        DESCRIPTION:
            Display a summary of analyzer operations.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        report_path = self.path_info["report_path"]


        print "\n=============================================================="
        print "Ebook archive analyzed!".center(80)
        print "Title\t: %s" % self.title
        print "Report directory\t: %s" % report_path
        print "================================================================"

