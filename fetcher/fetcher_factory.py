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
#import re
import urllib2
import zipfile
import shutil
import StringIO
from lxml import etree as etree


from shared import file_operations as FileOperations
from shared import xml_operations as XMLOperations
from shared import git_handler as GitHandler

from converter import parser_runeberg as ParserRuneberg


# ==========================================================================
# CLASS:
#   FetcherFactory
#
# CONSTRUCTOR:
#   title
#   valid_domains
#   args
#
# CLASS VARIABLES:
#   DOC_XHTML
#   css_book_template_file  
#   css_link_file
#
# DESCRIPTION:
# ==========================================================================
class FetcherFactory(object):
    """
    DESCRIPTION:

    PARAMETERS:
    """
    
    DOCTYPE_XHTML = ( "<!DOCTYPE html PUBLIC "
                      "\"-//W3C//DTD XHTML 1.1//EN\" " 
                      "\"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">" )

    # templates for working directory
    css_book_template_file = "fetcher/resources/book.css"

    # css file relative to working dir path
    css_link_file = "css/book.css"

    
    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(self, title, path_info, valid_domains)
    # ==========================================================================
    def __init__(self, title, path_info, valid_domains):
        self.title = title
        self.path_info = path_info
        self.valid_domains = valid_domains
        
        # external classes
        self.parser_runeberg = ParserRuneberg.ParserRuneberg(title, path_info)
        self.file_operations = FileOperations.FileOperations()
        self.xml_operations = XMLOperations.XMLOperations()
        self.git_handler = GitHandler.GitHandler()


        # parsed articles
        self.articles = None
    
    # ==========================================================================
    # METHOD:
    #   fetch_ebook_source(URL)
    # ==========================================================================
    def fetch_ebook_source(self, url):
        """
        DESCRIPTION:
            Fetch ebook source FROM HTTP source or file in local folder.
            
        PARAMETERS:
            URL     string      URL or filename source.
        
        RETURN: 
            archive_path    string      Path to source archive
        """
        archive_path = self.path_info["archive_path"]
        archive_full_path = None


        # filename is provided instead of URL
        if "http" not in url and "zip" in url:
            # extract filename
            filename = os.path.basename(url)
            archive_full_path = archive_path + filename
            shutil.copy2(url, archive_full_path)
            return archive_full_path
        

        # validate download origin, if false, then exit
        # application with error message
        try:
            if not self.validate_url_source(url):
                sys.stderr.write("[ERROR]: domain name is invalid\n")
                sys.exit(1)
        except NotImplementedError:
            print "[FATAL] URL validation not implemented"
            sys.exit(1)

        # download input file
        archive_name, archive = FetcherFactory.download_archive(url)
        
        # write file to workspace
        archive_full_path =  archive_path + archive_name 
        self.file_operations.write_archive(archive_full_path, archive)
            
        return archive_full_path
        


    # ==========================================================================
    # METHOD:
    #   download_archive(URL)
    # ==========================================================================
    @staticmethod
    def download_archive(url):
        """
        DESCRIPTION:
            Download URL archive.
            
        PARAMETERS:
            url     string      URL source.
        
        RETURN: 
            archive_name    string      Name of archive
            archive         string      File-like archive
        """
        print "[STATUS] Get Ebook archive..."
        if "mode=txtzip" not in url:
            print "[ERROR] Wrong archive"
            print "You should download the \"All text and index files\" version"
            sys.exit(1)

        # open and read remote archive
        try:
            response  = urllib2.urlopen(url)
            archive = response.read()
        except urllib2.URLError as err:
            print "[ERROR] openening remote archive: ", err
            sys.exit(1)

        # parse the rfc822.Message object
        msg = response.info()
        fileinfo = msg.getheader('Content-disposition')
        if fileinfo is None:
            print "[ERROR] could not open archive header"
            sys.exit(1)

        # extract the archive name
        archive_name = fileinfo.split("=")[1]
       
        return (archive_name, archive) 
   
    # ==========================================================================
    # METHOD:
    #   extract_archive(archive_path)
    # ==========================================================================
    def extract_archive(self, archive_path):
        """
        DESCRIPTION:
            Extract the zip archive.
            
        PARAMETERS:
            archive_path    string      Path to archive
        
        RETURN: 
            void
        """
        print "[STATUS] Extracting Project Runeberg archive... "
        original_path = self.path_info["original_path"]

        try:
            # create zip object
            archive = zipfile.ZipFile(archive_path)
            
            # extracting validated files to original folder
            archive.extractall(original_path)
            
        except zipfile.BadZipfile as bzf:
            print "Error extracting: ", bzf
        

    # ==========================================================================
    # METHOD:
    #   convert_working_to_xhtml(self)
    # ==========================================================================
    def convert_working_to_xhtml(self):
        """
        DESCRIPTION:
            Best effort conversion of HTML files to XHTML files using
            lxml HTMLParser().
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        print "[STATUS] Automatic XHTML conversion in working directory... "

        title = "Auto-generated XHMTL"
        original_path = self.path_info["original_path"]
        working_path = self.path_info["working_path"]
        

        # check if staging already exists
        if not os.path.exists(working_path):
            # copy all files from original to staging
            shutil.copytree(original_path, working_path)

        # parsed articles
        self.articles = self.parser_runeberg.parse_articles_lst()


        # convert all HTML files to XHTML
        all_html_files = self.file_operations.list_files(working_path, "*.html")
        for filename in all_html_files:
           
            try:
                # create HTML, TITLE, CSS link, META, body XHTML skeleton
                #filename_only = self.file_operations.filename_only_final(filename) 
                
                # parse HTML and output well-formed HTML
                html = self.file_operations.read_file(filename)
                parser = etree.HTMLParser()
                tree_orig = etree.parse(StringIO.StringIO(html), parser)
                
                
                #for key,value in chapters.iteritems():
                for article in self.articles:
                    if os.path.basename(filename) in article:
                        title = article[2]
                
                
                # append parsed body to xhtml skeleton
                tree = self.xml_operations.build_xhtml_skel_final(title, self.css_link_file)
                root_orig = tree_orig.getroot()
                root = tree.getroot()
                #body_orig = root_orig.find('body')
                root.append(root_orig.find('body'))
               

                # serialize the XML to Unicode strings
                # lxml versions older than 2.3 does not support doctype keyword
                if "2.3" in etree.__version__[:3]:
                    root_unicode = etree.tostring(  root, encoding=unicode, 
                                                    pretty_print=True, 
                                                    doctype=self.DOCTYPE_XHTML )
                else:
                    root_unicode = etree.tostring(  root, encoding=unicode, 
                                                    pretty_print=True   )

                
                # write xml tree to file
                self.file_operations.write_file(filename, root_unicode)
            
            except UnicodeDecodeError as err:
                print "[ERROR] XHTML conversion could not decode document"
                print "Check encoding: ", os.path.basename(filename)

            except etree.XMLSyntaxError as err:
                print "[ERROR] XHTML conversion failed: ", os.path.basename(filename), err


    
    
    # ==========================================================================
    # METHOD:
    #   setup_repo(message)
    # ==========================================================================
    def setup_repo(self, message):
        """
        DESCRIPTION:
            Initialize, add and commit files to a Git repository.
            
        PARAMETERS:
            message     string      Commit message
        
        RETURN: 
            void
        """
        
        print "[STATUS] GIT operations... "
        working_path = self.path_info["working_path"]
        
        # move into working directory
        os.chdir(working_path)
        
        # initalize git repo
        if not os.path.exists(".git"):
            self.git_handler.init()
            
            # add all files to repo
            self.git_handler.add_all()
            
            # commit and tag orignal files
            self.git_handler.commit(message)
            
            self.git_handler.tag("init", "original files from Project Runeberg")

        else:
            # add all files to repo
            self.git_handler.add_all()
            
            # commit and tag orignal files
            self.git_handler.commit(message)



    # ==========================================================================
    # ABSTRACT METHOD:
    #   update_source_info()
    # ==========================================================================
    def update_source_info(self):
        """
        DESCRIPTION:
            Abstract method, implemented in subclasses.
            
        PARAMETERS:
            message     string      Commit message
        
        RETURN: 
            void
        """
        raise NotImplementedError( "No implementation available" )
    
    # ==========================================================================
    # ABSTRACT METHOD:
    #   validate_URL_source(url)
    # ==========================================================================
    def validate_url_source(self, url):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        raise NotImplementedError( "No implementation available" )
    
    # ==========================================================================
    # ABSTRACT METHOD:
    #   validate_archive(archive_path)
    # ==========================================================================
    def validate_archive(self, archive_path):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        raise NotImplementedError( "No implementation available" )
    
    # ==========================================================================
    # ABSTRACT METHOD:
    #   construct_working_directory(auto_markup, auto_populate)
    # ==========================================================================
    def construct_working_directory(self, auto_markup, auto_populate):
        """
        DESCRIPTION:
            Abstract method, implemented in subclasses.
            
        PARAMETERS:
            message     string      Commit message
        
        RETURN: 
            void
        """

        raise NotImplementedError( "No implementation available" )
    
