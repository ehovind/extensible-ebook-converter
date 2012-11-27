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

import re
import zipfile
import os
import shutil
import codecs
from lxml import etree as etree

from . fetcher_factory import FetcherFactory as FetcherFactory

# ==========================================================================
# CLASS:
#   FetcherRuneberg
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class FetcherRuneberg(FetcherFactory):
    """
    DESCRIPTION:

    PARAMETERS:
    """


    URL_authors = "http://runeberg.org/authors/a.lst"
    URL_titles = "http://runeberg.org/authors/t.lst"

    format_files = ("Articles.lst", "Metadata")




    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(self, title, path_info, valid_domains)
    # ==========================================================================
    def __init__(self, title, path_info, valid_domains):
        FetcherFactory.__init__(self, title, path_info, valid_domains)
        


    # ==========================================================================
    # METHOD:
    #   validate_url_source(url)
    # ==========================================================================
    def validate_url_source(self, url):
        """
        DESCRIPTION:
            Validate URL input source.
            Requirements:
            - return True when URL included in validDomains
            - return False when URL not included in validDomains
            - return False when URL is not an URL
            Process command line arguments.
            
        PARAMETERS:
            URL         string      URL source string.
        
        RETURN: 
            valid       boolean     True if valid domain, False if not.
        """
        domain = None

        # extract the domain from the string
        try:
            domain_format = \
                re.compile(ur'^(http://|https://)?[w]{0,3}\.?([\w\d\-\.]+\.[a-z]{2,6})\/?')
            match = domain_format.search(url)

            if not match:
                raise IndexError
                        
            domain = match.group(2)

        except IndexError as err:
            print("[ERROR]: Could not extract domain name: "), err
            return False

        # there is a match, check if domain is valid
        if domain in self.valid_domains:
            return True
        
        return False



    # ==========================================================================
    # METHOD:
    #   validate_archive(archive_path)
    # ==========================================================================
    def validate_archive(self, archive_path):
        """
        DESCRIPTION:
            Validate input archive. Search for Project Runeberg specific files.
            
        PARAMETERS:
            archive_path    string      Path to zip archive.
        
        RETURN: 
            void
        """
        print "[STATUS] Validating Project Runeberg archive... ",
        
        # validate zip archive
        if os.path.isfile(archive_path):
            try:
                # create zip object
                archive = zipfile.ZipFile(archive_path)
            
                # get a list of members in archive
                members = archive.namelist()

                # check for Runeberg files
                for member in members:

                    if member in self.format_files:
                        print member, "(found)"
                        return True
                
            except zipfile.BadZipfile as bzf:
                print "Error validating archive: ", bzf
        
        # validate file path
        if os.path.isdir(archive_path):
            all_files = self.file_operations.list_files(archive_path, "*")
            for filename in all_files:
                if os.path.basename(filename) in self.format_files:
                    print os.path.basename(filename), "(found)"
                    return True

        return False

        


    # ==========================================================================
    # METHOD:
    #   is_markup_present()
    # ==========================================================================
    def is_markup_present(self):
        """
        DESCRIPTION:
            Check Articles.lst if minimal markup is present.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        # check that all articles have populated content
        for article in self.articles:
            # no filename is registered for this article
            if article[1] is None:
                return False
        
        return True
        
        



    # ==========================================================================
    # METHOD:
    #   construct_working_directory(auto_markup, auto_populate)
    # ==========================================================================
    def construct_working_directory(self, auto_markup, auto_populate):
        """
        DESCRIPTION:
            Construct a working directory. Copy publication files from original folder.
            Populate the working directory with css and an images folder.
            Auto-markup the files to XHMTL if paramterer is True.
            Auto-populate with files from Pages if parameter is True.
            
        PARAMETER:
            auto_markup     boolean     Automatic conversion HTML to XHTML.
            auto_populate   boolean     Automatic creation of mininaml XHTMK.
        
        RETURN: 
            void
        """
        
        print "[STATUS] Construct working directory... "
        original_path = self.path_info["original_path"]
        working_path = self.path_info["working_path"]
        images_path = self.path_info["images_path"]
        css_path = self.path_info["css_path"]



      
        # if working_directory exists, do not modify anything
        if not os.path.exists(working_path):
            # copy files from original to working_directory
            shutil.copytree(original_path, working_path, 
                    ignore=shutil.ignore_patterns('*Pages*'))

        #
        # create images folder
        #
        if not os.path.exists(images_path):
            os.mkdir(images_path)

        #
        # create css folder and template
        #
        if not os.path.exists(css_path):
            os.mkdir(css_path)
            
            # copy template css
            shutil.copy2(self.css_book_template_file, css_path + "book.css")

        #
        # populate working dir with files from Pages/
        #
        if auto_populate:
            self.populate_working_directory()

            # return in case both arguments are set by user
            return

        # convert HTML to minimal XHTML 
        if auto_markup:
            self.convert_working_to_xhtml()

    
    


    # ==========================================================================
    # METHOD:
    #   update_source_info(self):
    # ==========================================================================
    def update_source_info(self):
        """
        DESCRIPTION:
            Update Project Runeberg a.lst and t.lst files.
            http://runeberg.org/authors/a.lst
            http://runeberg.org/authors/t.lst
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        print "[STATUS] Updating Project Runeberg information... ",
        info_path = self.path_info["info_path"]
        

        authors_info_path = info_path + "a.lst"
        titles_info_path = info_path + "t.lst"

      
        # download Author information
        self.file_operations.download_file(authors_info_path, self.URL_authors)
        
        # download Title information
        self.file_operations.download_file(titles_info_path, self.URL_titles)

        print "done."
    
    
    # ==========================================================================
    # METHOD:
    #   populate_working_directory()
    # ==========================================================================
    def populate_working_directory(self):
        """
        DESCRIPTION:
            Populate working directory with scanned text files from Pages/
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        print "[STATUS] Populating working directory from Pages/ ..."

        original_path = self.path_info["original_path"]
        working_path = self.path_info["working_path"]


            
        # parsed articles
        self.articles = self.parser_runeberg.parse_articles_lst()
        
        # check if HTML files with chapters already created
        if self.is_markup_present():
            print "not needed."
            return 

        # no markup files are created, try to construct a minimalistic version
        # add all chaptes
        for article in self.articles:

            chapter_type = article[0]
            chapter_filename = article[1]
            title = article[2]
            
            # article needs autopopulating
            if chapter_filename is None:
                # build head of chapter and first page
                tree = \
                    self.xml_operations.build_xhtml_skel_final(title, self.css_link_file)
            
                # add each page in chapter
                pages_in_chapter = article[3]

                # fill out page range
                start = int(pages_in_chapter[0])
                if (pages_in_chapter[1]) is not None:
                    stop = int(pages_in_chapter[1])
                else:
                    stop = start
                page_interval = list()

                while start <= stop:
                    number = str(start)
                    number_string = number
                    while len(number_string) < 4:
                        number_string = "0" + number_string
                    page_interval.append(number_string)
                    start += 1
            
                # add each page in chapter to chapter file
                for page_number in page_interval:

                    # read text from file
                    txt_path = original_path + "Pages/" + page_number +".txt"
                    text = self.file_operations.read_unicode_final(txt_path) 

                    # insert chapter text
                    self.xml_operations.insert_paragrap_into_XHTML_final(tree, int(page_number), text)

                
                # serialize the XML to Unicode strings
                # lxml versions older than 2.3 does not support doctype keyword
                if "2.3" in etree.__version__[:3]:
                    root_unicode = etree.tostring(  tree.getroot(), 
                                                    encoding=unicode, 
                                                    pretty_print=True, 
                                                    doctype=self.DOCTYPE_XHTML )
                else:
                    root_unicode = etree.tostring(  tree.getroot(), 
                                                    encoding=unicode, 
                                                    pretty_print=True )
            
                # write xml tree to file
                markup_file = working_path + chapter_type + ".html"
                self.file_operations.write_unicode_final(markup_file, root_unicode)
        
        # update Articles.lst
        self.update_articles_lst()



    
    # ==========================================================================
    # METHOD:
    #   update_articles_lst()
    # ==========================================================================
    def update_articles_lst(self):
        """
        DESCRIPTION:
            Update Articles.lst after populating working directory.
            
        PARAMETERS:
            None
        
        RETURN: 
            void
        """
        articles_path = self.path_info["articles_path"]

        try:
            with codecs.open(articles_path, "w", encoding="utf-8") as f:
                # update heading
                line = "#" + self.title + "/Articles.lst\n"
                f.write(line)
                
                # write each article
                for article in self.articles:
                    chapter_type = article[0]
                    chapter_filename = article[1]
                    chapter_title = article[2]

                    if chapter_filename is None:
                        chapter_filename = chapter_type
                    else:
                        chapter_filename = chapter_filename.strip(".html")
                    
                    # convert page_interval to runeberg number string format
                    pages_in_chapter = article[3]
                    page_start = pages_in_chapter[0]
                    page_stop = pages_in_chapter[1]
                    
                    if page_start is not None:
                        while len(page_start) < 4:
                            page_start = "0" + page_start

                    if page_stop is not None:
                        while len(page_stop) < 4:
                            page_stop = "0" + page_stop

                    
                    # construct article line
                    line = """%s|%s|%s-%s\n""" % \
                            ( chapter_filename, 
                              chapter_title,
                              str(page_start), str(page_stop))

                    f.write(line)
                    
                f.close()

        except IOError as err:
            print "except", err




