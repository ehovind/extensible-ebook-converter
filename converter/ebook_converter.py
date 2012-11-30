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

from converter import parser_runeberg as ParserRuneberg
from converter import ebook_epub as EbookEpub

from shared import file_operations as FileOperations
from shared import xml_operations as XMLOperations
from shared import git_handler as GitHandler
# ==========================================================================
# CLASS:
#   EbookConverter
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class EbookConverter(object):
    """
    DESCRIPTION:
    
    PARAMETERS:
    """
   

    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(workspace, args)
    # ==========================================================================
    def __init__(self, workspace, args):
        self.workspace = workspace
        self.args = args
        
        # parsed arguments
        self.title = None
        self.output_format = "epub"
        self.compress_only = False

        # workspace path info
        self.path_info = dict() 

        # external classes
        self.file_operations = FileOperations.FileOperations()
        self.xml_operations = XMLOperations.XMLOperations()
        self.git_handler = GitHandler.GitHandler()


    
    # ==========================================================================
    # METHOD:
    #   process()
    # ==========================================================================
    def process(self):
        """
        DESCRIPTION:
            Test. 
        PARAMETERS:
            None
        RETURN: 
            void
        """
        ebook_source = None
        parser = None

        # parse configuration
        self.parse_config()

        #
        # prepare workspace
        # create folder struture and path info
        self.path_info = self.prepare_path_info(self.title)
        self.prepare_workspace_folders()
        

        #
        # parse runeberg data
        #
        #if not os.path.exists(self.working_path):
        try:
            parser = ParserRuneberg.ParserRuneberg(self.title, self.path_info)
        
            # check publication
            parser.check_publication()

            # parse the source
            ebook_source = parser.parse_source()
        except NotImplementedError:
            print "[FATAL] Parser not implmented"
            sys.exit(1)

        
        #
        # build ebook
        #
        if self.output_format == "epub":
            ebook = EbookEpub.EbookEpub(self.path_info, ebook_source)
        else:
            print "[FATAL] only supported format is ePub"
            sys.exit(1)
        
        # compress only after manual modifications
        if self.compress_only:
            try:
                ebook.compress()
            except NotImplementedError:
                print "[FATAL] Ebook builder not impermented"
                sys.exit(1)
            

        # parse preface, chapters and build container
        else:
            try:
                # buld ebook container
                ebook.build()
                # compress the ebook according to specifications
                # NOTE: chdirs into workspace
                ebook.compress()
            except NotImplementedError:
                print "[FATAL] Ebook builder not implemented"
                sys.exit(1)
   

        #
        # create patches
        #
        self.create_patches("Committing modified files (eecon_converter)")


        # display summary
        self.display_summary()

        

    # ==========================================================================
    # METHOD:
    #   parse_config()
    # ==========================================================================
    def parse_config(self):
        """
        DESCRIPTION:
            Test. 
        PARAMETERS:
            None
        RETURN: 
            void
        """

        #if "auto" in self.args:
        #    self.auto_mode = self.args['auto']


        # set publication title
        if "title" in self.args:
            if self.args['title'] is None:
                print "[ERROR] define a tile with --title TITLE"
                sys.exit(1)
            self.title = self.args["title"]

        if "output_format" in self.args:
            if self.args['output_format'] is not None:
                self.output_format = self.args['output_format']
        
        if "compress_only" in self.args:
            self.compress_only = self.args["compress_only"]






    
    # ==========================================================================
    # METHOD:
    #   prepare_workspace()
    # ==========================================================================
    def prepare_path_info(self, title):
        """
        DESCRIPTION:
            Test. 
        PARAMETERS:
            None
        RETURN: 
            void
        """
       
        books_path  = self.workspace + "/books/"


        path_info = {   
            "books_path"    : books_path, 
            "info_path"     : self.workspace + "/info/",
            "archive_path"  : books_path + title + "/input/archive/",
            "original_path" : books_path + title + "/input/original/",
            "working_path"  : books_path + title + "/input/working_directory/",
            "output_path"   : books_path + title + "/output/ebooks/", 
            "patch_path"    : books_path + title + "/output/patches/" }

        return path_info


    # ==========================================================================
    # METHOD:
    #   prepare_workspace()
    # ==========================================================================
    def prepare_workspace_folders(self):
        """
        DESCRIPTION:
            Test. 
        PARAMETERS:
            None
        RETURN: 
            void
        """
        working_path = self.path_info["working_path"]
        books_path = self.path_info["books_path"]
        output_path = self.path_info["output_path"]
        patch_path = self.path_info["patch_path"]


        if not os.path.exists(working_path):
            print "[ERROR] this title is not fetched"
            print "Available titles: ", os.listdir(books_path)
            sys.exit(1)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if not os.path.exists(patch_path):
            os.makedirs(patch_path)
        
    
    

    # ==========================================================================
    # METHOD:
    #   create_patches(message)
    # ==========================================================================
    def create_patches(self, message):
        """
        DESCRIPTION:
            Test. 
        PARAMETERS:
            None
        RETURN: 
            void
        """
        
        print "[STATUS] Creating patches from modified files in working directory... ",
        working_path = self.path_info["working_path"]
        
        # enter repo
        os.chdir(working_path)
        
        # commit current files in working directory
        self.git_handler.add_all()

        # commit current state of working directory
        self.git_handler.commit(message)

        # create a patch against "init" tag.
        patch_file = "../../output/patches/" + self.title +".patch"
        self.git_handler.format_patch(patch_file)

        print "done."
    
   
    # ==========================================================================
    # METHOD:
    #   display_summary()
    # ==========================================================================
    def display_summary(self):
        """
        DESCRIPTION:
            Display summary information.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        output_path = self.path_info["output_path"]

        print "\n=============================================================="
        print "Ebook archive created!\n".center(80)
        print "Title\t: %s" % self.title
        print "Format\t: %s" % "ePub"
        print "Output\t: %s\n" % output_path
        print "Validate ePub on http://validator.idpf.org/ or use EpubCheck"
        print "Convert to Amazon kindle format with the proprietary tool KindleGen"
        print "================================================================"










