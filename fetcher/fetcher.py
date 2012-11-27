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
import re
#import urllib2
import shutil
import subprocess
import sys
#from lxml import etree as etree

from . import fetcher_runeberg as FetcherRuneberg
from shared import file_operations as FileOperations
#from shared import xml_operations as XMLOperations
from shared import git_handler as GitHandler
from analyzer import analyzer_unicode as AnalyzerUnicode

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
class Fetcher(object):
    """
    DESCRIPTION:

    PARAMETERS:
    """

    
    dependencies =  {   "lxml"      :   "library",
                        "iconv -v"  :   "external"  }

    
    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(self, workspace, valid_domains, args)
    # ==========================================================================
    def __init__(self, workspace, valid_domains, args):
        self.workspace = workspace
        self.valid_domains = valid_domains
        self.args = args
        
        # parsed arguments
        self.title = None
        self.source = None
        self.auto_utf8 = False
        self.auto_markup = False
        self.auto_populate = False
        self.patch = None
        
        # workspace path information
        self.path_info = dict()

        # external classes
        self.file_operations = FileOperations.FileOperations()
        self.git_handler = GitHandler.GitHandler()
        self.analyzer_unicode = None
    
    
    # ==========================================================================
    # METHOD:
    #   process()
    # ==========================================================================
    def process(self):
        """
        DESCRIPTION:
            Process command line arguments.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """

        # check dependencies
        self.check_dependencies()

        # parse command line arguments
        self.parse_config()

        # prepare main workspace structure
        self.path_info = self.prepare_path_info(self.title)
        
        # prepare main workspace structure
        self.prepare_workspace_folders()
        
        # set some local variables
        books_path = self.path_info["books_path"]
        info_path = self.path_info["info_path"]
        working_path = self.path_info["working_path"]
        
        # create a Runeberg fetcher object
        fetcher_runeberg = FetcherRuneberg.FetcherRuneberg(self.title, 
                self.path_info, self.valid_domains)
        
        # fetch Runeberg a.lst and t.lst 
        try:
            authors_info_path = info_path + "a.lst"
            titles_info_path = info_path + "t.lst"
            if not os.path.exists(authors_info_path) or not os.path.exists(titles_info_path):
                fetcher_runeberg.update_source_info()
        except NotImplementedError:
            print "[FATAL] Construction of working directory not implemented"
            sys.exit(1)

        self.analyzer_unicode = AnalyzerUnicode.AnalyzerUnicode(self.path_info, "file")


        #
        # fetch a source archive
        #
        if not self.source is None:
            # check if source title is already downloaded
            if self.check_title_exists():
                print "[ERROR] this title is already fetched, exiting..."
                sys.exit(1)
            
            
            # download archive
            archive_path = fetcher_runeberg.fetch_ebook_source(self.source)
            
            # validate ebook source
            try:
                if not fetcher_runeberg.validate_archive(archive_path):
                    print "[FATAL] Archive is not valid"
                    sys.exit(1)
            except NotImplementedError:
                print "[FATAL] Validation of archive not implemented"
                sys.exit(1)
            
            # extract archive
            fetcher_runeberg.extract_archive(archive_path)
            
            # copy original files to working directory and if selected
            # prepare minimal XHTML from or
            # populate working directory from files in Pages
            try:
                fetcher_runeberg.construct_working_directory(self.auto_markup,
                        self.auto_populate)
            except NotImplementedError:
                print "[FATAL] Construction of work directory not implemented"
                sys.exit(1)


            # initialize and tag git repo with original files
            fetcher_runeberg.setup_repo("Initial commit of original files")
            
            self.display_summary()


        #
        # automatic conversion or create miniamal XHMTL from Pages
        #
        if self.auto_markup or self.auto_populate:
            # check if title is fetched
            if not self.check_title_exists():
                print "[FATAL] this title is not fetched. ", 
                print "Available titles: ", os.listdir(books_path)
                sys.exit(1)
            
            # check for utf-8 encoding
            if not self.analyzer_unicode.validate_encoding():
                print "[FATAL] non utf-8 encoding detected"
                print "[FATAL] Suggestion: convert with --auto-utf8"
                sys.exit(1)
            
            # validate ebook source
            try:
                if not fetcher_runeberg.validate_archive(working_path):
                    print "[FATAL] Archive is not valid"
                    sys.exit(1)
            except NotImplementedError:
                print "[FATAL] Validation of archive not implemented"
                sys.exit(1)

            # parse article information

            # copy original files to working directory and if selected
            # prepare minimal XHTML from or
            # populate working directory from files in Pages
            try:
                fetcher_runeberg.construct_working_directory(self.auto_markup, self.auto_populate)
            except NotImplementedError:
                print "[FATAL] Construction of working directory not implemented"
                sys.exit(1)

            if self.auto_markup:
                message = "Automatic markup fix of files in working directory"
            
            if self.auto_populate:
                message = "Automatic populating in working directory"

            # initialize and tag git repo with original files
            fetcher_runeberg.setup_repo(message)

        #
        # automatic conversion to UTF-8 using iconv
        #
        if self.auto_utf8:
            self.auto_convert_utf8()



        #
        # apply git patch
        #
        if not self.patch is None:
            # check if title is fetched
            if not self.check_title_exists():
                print "[ERROR] this title is not fetched. ", 
                print "Available titles: ", os.listdir(books_path)
                sys.exit(1)
            
            # apply git patch to working directory
            self.apply_patch()


    # ==========================================================================
    # METHOD:
    #   parse_config()
    # ==========================================================================
    def parse_config(self):
        """
        DESCRIPTION:
            Parse arguments.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        

        if "auto_utf8" in self.args:
            self.auto_utf8 = self.args["auto_utf8"]

        if "auto_markup" in self.args:
            self.auto_markup = self.args["auto_markup"]

        if "auto_populate" in self.args:
            self.auto_populate = self.args["auto_populate"]
        if "patch" in self.args:
            self.patch = self.args["patch"]

        # extract title 
        if "source" in self.args:
            self.source = self.args["source"]
            self.title = self.extract_title(self.args["source"])
        
        if "title" in self.args and self.title is None:
            self.title = self.args["title"]

        if self.title is None:
            print "[ERROR] could not extract title, define with --title TITLE"
            sys.exit(1)

        return self.title

    # ==========================================================================
    # METHOD:
    #   prepare_workspace_path_info()
    # ==========================================================================
    def prepare_path_info(self, title):
        """
        DESCRIPTION:
            Parse arguments into path information.
            
        PARAMETERS:
            None
        
        RETURN: 
            path_info   dict        Path information
        """

        # insert all parsed arguments in path_info
        books_path  = self.workspace + "/books/"
        original_path = books_path + title + "/input/original/"
        working_path = books_path + title + "/input/working_directory/"

        path_info = {   
            "books_path"    : self.workspace + "/books/", 
            "info_path"     : self.workspace + "/info/",
            "archive_path"  : books_path + title + "/input/archive/",
            "original_path" : original_path,
            "working_path"  : books_path + title + "/input/working_directory/",
            "output_path"   : None,
            "report_path"   : None,
            "css_path"      : working_path + "/css/",
            "images_path"   : working_path + "/images/",
            "cover_file"    : None,
            "patch_path"    : None,
            "articles_original_path" : original_path + "Articles.lst",
            "articles_path" : working_path + "Articles.lst"
        }

        return path_info


    # ==========================================================================
    # METHOD:
    #   prepare_workspace_folders()
    # ==========================================================================
    def prepare_workspace_folders(self):
        """
        DESCRIPTION:
            Create workspace folders.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        books_path = self.path_info["books_path"]
        info_path = self.path_info["info_path"]
        archive_path = self.path_info["archive_path"]
        original_path = self.path_info["original_path"]

        
        if not os.path.exists(books_path):
            os.makedirs(books_path)

        if not os.path.exists(info_path):
            os.makedirs(info_path)

        if not os.path.exists(archive_path):
            os.makedirs(archive_path)

        if not os.path.exists(original_path):
            os.makedirs(original_path)


    # ==========================================================================
    # METHOD:
    #   extract_title()
    # ==========================================================================
    def extract_title(self, source):
        """
        DESCRIPTION:
            Extract title from input source. URL or Filename
            
        PARAMETERS:
            source  string      URL or Filename
        
        RETURN: 
            title   string      Title of ebook
        """
        title = None

        if source is None:
            return

        # extrac title from URL
        # Format:
        # http://runeberg.org/download.pl?mode=txtzip&work=herrgard
        if "http" in source:
            url_format = re.compile("^http://.*download.pl.*work=(\w+)$")
            match = url_format.search(source)
            if match:
                title = match.group(1)
        # filename
        # Format:
        # incoming/herrgard-txt.zip
        else:
            file_name_format = re.compile(ur'\/?([\w]+)\-txt.zip$')
            match = file_name_format.search(source)
            if match:
                title = match.group(1)

        return title

        


    # ==========================================================================
    # METHOD:
    #   auto_convert_utf8()
    # ==========================================================================
    def auto_convert_utf8(self):
        """
        DESCRIPTION:
            Auto convert file encoding to UTF-8
            
        PARAMETERS:
            none
        
        RETURN: 
            void
        """
        print "[STATUS] Automatic UTF-8 conversion in working directory... ",
        working_path = self.path_info["working_path"]

        publication_files = self.file_operations.list_publication_files(working_path)

        # temporary folder
        tmp = working_path + "out"
        if not os.path.exists(tmp):
            os.mkdir(tmp)

        # convert each publication file
        for filename in publication_files:

            # check if already utf-8
            if self.analyzer_unicode.analyze(filename)["encoding"] == "utf-8":
                continue

            out_file = tmp + "/"  + os.path.basename(filename)

            cmd = ['iconv', '-f', 'ISO-8859-1', '-t', 'UTF-8', 
                    filename, '-o', out_file]
            subprocess.call(cmd)
            
            # move converted file to working_directory
            shutil.move(out_file, filename)

        # remove tmp directory
        try:
            os.rmdir(tmp)
        except OSError:
            print "could not remove tmp directory"

        print "done."
        

    
    
    # ==========================================================================
    # METHOD:
    #   apply_path()
    # ==========================================================================
    def apply_patch(self):    
        """
        DESCRIPTION:
            Apply Git patch to source files in working directory.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        print "[STATUS] Applying patch... " + self.args["patch"]
        patch =  self.args["patch"]
        working_path = self.path_info["working_path"]
        books_path = self.path_info["books_path"]

        if not self.check_title_exists():
            print "[FATAL] this title is not fetched. ", 
            print "Available titles: ", os.listdir(books_path)
            sys.exit(1)
        
        apply_patches = ""
        
        
    
        try:
            # copy temp patch to working directory
            shutil.copy(patch, working_path)
        
            # change into working directory for git operations
            os.chdir(working_path)

        except IOError:
            print "[ERROR] this title is not fetched"
            sys.exit(1)

        # check patch integrity and actions 
        patch_filename = self.file_operations.filename_only_final(patch)
        self.git_handler.check_patch(patch_filename)

        # await user interaction
        while apply_patches != 'y' and apply_patches != 'n':
            apply_patches = raw_input("\n\tApply patch? (y)es or (n)o: ")
    
        # user has chosen to apply patch
        if apply_patches == 'y':
            self.git_handler.apply_patch(patch_filename)
            
        # remove temp patch file
        os.remove(patch_filename)
        
    
    # ==========================================================================
    # METHOD:
    #   check_title_exists() 
    # ==========================================================================
    def check_title_exists(self):
        """
        DESCRIPTION:
            Check if title already exists in workspace.
            
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
    #   check_dependencies()
    # ==========================================================================
    def check_dependencies(self):
        """
        DESCRIPTION:
            Process command line arguments.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        print "[STATUS] searching for dependencies... ",
        
        if len(Fetcher.dependencies.keys()) is 0:
            print "ok."
            return

        for tool in Fetcher.dependencies.keys():
            dependency = Fetcher.dependencies[tool]

            # check if python library is installed
            if dependency is "library":
                try:
                    __import__ (tool)
                except ImportError:
                    print "[FATAL] No libary: ", tool
                    sys.exit(1)
            
            # check if external binary exists
            if dependency is "external":
                try:     
                    # binary tool has an argument
                    if " -" in tool:
                        command = tool.split(" ")[0]
                        argument = tool.split(" ")[1]
                        cmd = [command, argument]
                        # call tool, redirect stdout and stderr to /dev/null
                        subprocess.call(cmd, stdout=open(os.devnull,'w'),
                                stderr=subprocess.STDOUT)
                    else:
                        # call tool, redirect stdout and stderr to /dev/null
                        subprocess.call(tool, stdout=open(os.devnull,'w'),
                                stderr=subprocess.STDOUT)

                except OSError as err:
                    print "[FATAL] No binary: ", tool, err
                    sys.exit(1)

        print "ok. "
    
    # ==========================================================================
    # METHOD:
    #   display_summar()
    # ==========================================================================
    def display_summary(self):
        """
        DESCRIPTION:
            Display summary of fetching process.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        working_path = self.path_info["working_path"]


        print "\n=============================================================="
        print "Ebook archive fetched and initalized!".center(80)
        print "Title\t: %s" % self.title
        print "Format\t: %s" % "Project Runeberg"
        print "Work directory\t: %s" % working_path
        print "================================================================"
