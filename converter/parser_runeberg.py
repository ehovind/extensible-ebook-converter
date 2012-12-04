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

import codecs
import re
import sys
import os
from collections import deque
from datetime import date

#from parser_factory import ParserFactory as ParserFactory
from converter.parser_factory import ParserFactory as ParserFactory
from converter.source_runeberg import SourceRuneberg as SourceRuneberg
#from source_runeberg import SourceRuneberg as SourceRuneberg


# ==========================================================================
# CLASS:
#   ParserRuneberg(ParserFactory)
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class ParserRuneberg(ParserFactory):
    """
    DESCRIPTION:
    
    PARAMETERS:
    """
    
    format = "runeberg"
    rights  = "This work is known to be in the Public Domain"


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(title, path_info)
    # ==========================================================================
    def __init__(self, title, path_info):
        ParserFactory.__init__(self, title, path_info, format)
        self.title = title

        # workspace path info
        self.working_path =  path_info["working_path"]
        self.metadata_path = self.working_path + "Metadata"
        self.articles_lst_path = self.working_path + "Articles.lst"
        self.pages_lst_path = self.original_path + "Pages.lst"
        self.preface_path = self.working_path + "preface.html"
        
         
        # datastructures
        
        # pages info
        # [[number_of_pages : 0], {page_number : [html_file, adjusted_page_number]}]
        self.pages = [dict(), dict()]
        
        # all chapter information parsed from Articles.lst
        # [type, filename, title, page_interval()]
        self.articles = list()
        
        # supported publication structure elements
        # type : (known aliases)
        self.publication_structure = { 
            "toc"       : ("toc.html"),
            "foreword"  : ("foreword.html", "forord.html"),
            "preface"   : ("preface.html", "index.html"), 
            "epilogue"  : ("epilogue.html", "epilog.html"), 
            "colophon"  : ("colophon.html"), 
        }   


        # metadata info 
        # metadata: { 
        #    [dc_element, dc_value, dc_attribute, dc_attribute_value, lookup, dc_level,
        #     opf_attribute, opf_value, opf_level, (dc_aliases)] }
        self.metadata = {
            "title"         :   [   "title", None, None, None, None, 
                                    "must", None, None, None, 
                                    ("title",)   ],
            "identifier"    :   [   "identifier", None, "id", "BookId", None, 
                                    "must","scheme", None, "optional", 
                                    ("marc",)   ],
            "language"      :   [   "language", None, None, None, None, 
                                    "must", None, None, None, 
                                    ("language", "original_language",)   ],
            "date"          :   [   "date", None, None, None, None, 
                                    "optional", "event", "publication", "optional", 
                                    ("publishing_year",)   ],
            "date_ebook"    :   [   "date", date.today().isoformat(), None, None, None, 
                                    "optional", "event", "ebook-publication", "optional", 
                                    ("publishing_year_ebook",)   ],
            "creator"       :   [   "creator", [], None, None, [], 
                                    "should", "role", "aut", "optional", 
                                    ("authorkey",)   ],
            "contrib_trans" :   [   "contributor", None, None, None, None, 
                                    "should", "role", "trl", "optional", 
                                    ("translatorkey",)   ],
            "contrib_coaut" :   [  "contributor", None, None, None, None, 
                                    "should", "role", "aut", "optional", 
                                    ("coauthorkey",)   ],
            "source"        :   [   "source", "Project Runeberg", None, None, None, 
                                    "optional", None, None, None, 
                                    ("source",)   ],
            "rights"        :   [   "rights", self.rights, None, None, None, 
                                    "optional", None, None, None, 
                                    ("rights",)   ],
            "type"          :   [   "type", None, None, None, None, 
                                    "optional", None, None, None, 
                                    ("type",)   ]
        }




    # ==========================================================================
    # METHOD:
    #   parse_source():
    # ==========================================================================
    def parse_source(self):
        """
        DESCRIPTION:
            Parse Project Runeberg source publcation. 
        PARAMETERS:
            None
        RETURN: 
            ebook_source    EbookSourceRuneberg     Instance of publication.
        """
        print "[STATUS] Parsing runeberg archive... "

        # parse Pages.lst and search for page anchors in content
        self.parse_pages_lst()
        
        # parse metadata 
        self.parse_metadata()

        # chapter info like numbering and titles
        self.parse_articles_lst()

        # create an ebook_source instance
        ebook_source = SourceRuneberg(  self.title, self.metadata, 
                                        self.articles, self.pages   )
       
        return ebook_source




    # ==========================================================================
    # METHOD:
    #   parse_metadata()
    # ==========================================================================
    def parse_metadata(self):
        """
        DESCRIPTION:
            Parse the metadata in Metadata.
        PARAMETERS:
            None
        RETURN: 
            metadata    dict        Metadata elements.
        """
        print "[STATUS] Parse metadata from Runeberg source file... "
      
        #
        # parse metadata
        #
        try:
            with codecs.open(self.metadata_path, "r", encoding="utf-8") as f:

                # search metadata attributes and values
                # FORMAT: TITLE: Bannlyst
                metadata_format = re.compile('^(\w+)\:\s(.*)')

                # search all lines in file
                for line in f:
                    match = metadata_format.search(line)
                    if match:
                        metadata_key = match.group(1).lower()
                        metadata_value = match.group(2)

                        for key, value in self.metadata.iteritems():
                            aliases = value[9]

                            if metadata_key in aliases:
                                # populate the metadata dict
                                if isinstance(self.metadata[key][1], list):
                                    dc_values = metadata_value.split(",")
                                    for val in dc_values:
                                        # strip whitespace
                                        self.metadata[key][1].append(val.strip(' '))
                                else:
                                    self.metadata[key][1] = metadata_value
                                
                                # value added based on tuple, no duplication
                                break

                # Custom parsing of MARC
                # FORMAT: libris:7145869
                identifier = self.metadata["identifier"][1]
                if identifier is not None:
                    self.metadata["identifier"][7] = identifier.split(":")[0]
                    self.metadata["identifier"][1] = identifier.split(":")[1]
                    
                #
                # lookup additional author information from a.lst
                #
                
                # read a.lst with full author information 
                a_content = self.file_operations.read_lines_final(self.a_lst_path)

                for creator in self.metadata["creator"][1]:
                    search_string =  "|" + creator
                
                    # search for author key at the end of line
                    for line in a_content:
                        if line.endswith(u'%s\n'%search_string):
                            firstname = line.split('|')[3]
                            lastname = line.split('|')[2]
                            fullname = firstname + " " + lastname
                            self.metadata["creator"][4].append(fullname)
                  
        except (IOError, KeyError):
            print "[FATAL] Could not parse metadata"
            sys.exit(1)

        #print "PARSED metadata:",self.metadata
        return self.metadata



    # ==========================================================================
    # METHOD:
    #   parse_articles_lst()
    # ==========================================================================
    def parse_articles_lst(self):
        """
        DESCRIPTION:
            Parse article information from Articles.lst
        PARAMETERS:
            None
        RETURN: 
            articles    list    Article entries.
        """
        # 
        print "[STATUS] Parse chapter info from source files... "


        try:
            with codecs.open(self.articles_lst_path, "r", encoding="utf-8") as f:
                
                # seach for chapter numbering and titles
                articles_format = re.compile(
                        ur'([\d\w]+)?\|[\d+]?\.?([\w\-?\:?\s?\.()\d]+)\|(\d+)?-?(\d+)?', re.UNICODE)
                
                chapter_number = 1
                for line in f:
                    article_type = None
                    chapter_filename = None


                    match = articles_format.search(line)
                    if match:
                        
                        # set filename
                        if match.group(1) is not None:
                            chapter_filename = match.group(1) + ".html"
                        # did not find a matching format, fallback to linear numbering
                        # used 
                        #else:
                        #    chapter_filename = str(chapter_number) + ".html"
                        
                        # set chapter title
                        chapter_title = match.group(2)
                        
                        # set page interval
                        page_start = match.group(3)
                        page_stop = match.group(4)
                        page_interval = (page_start, page_stop)

                        # determine type
                        for key, value in self.publication_structure.iteritems():
                            if chapter_filename is not None:
                                if chapter_filename in value:
                                    article_type = key
                                    break
                            
                        # article type is a regular chapter
                        if article_type is None:
                            article_type = "chapter" + str(chapter_number)
                            chapter_number += 1
                            
                        # construct list item
                        chapter_info = [ article_type, chapter_filename,
                                         chapter_title, page_interval   ]

                        
                        # add to list
                        self.articles.append(chapter_info)

        except (IOError, KeyError):
            print "[FATAL] Could not parse Articles.lst, unknown format"
            sys.exit(1)


        #print "\n\nPARSED articles: ", self.articles

        return self.articles




    
    # ==========================================================================
    # METHOD:
    #   parse_pages_lst()
    # ==========================================================================
    def parse_pages_lst(self):
        """
        DESCRIPTION:
            Parse page information from Pages.lst
        PARAMETERS:
            None
        RETURN: 
            void
        """
        number_of_pages = 0 
        page_info = {}
        page_anchors = {}


        #
        # Find number of pages in publication
        #
        # 0240|238          (publication: karlekt)
        # 0244|Omslag       (publication: karlekt)
        pages_lst_format = re.compile(ur"^(\d+)\|[\w+|\d+]+$")
        try:
            with codecs.open(self.pages_lst_path, "r", encoding="utf-8") as f:

                # pop the last line of Pages.lst
                # Remove and return an element from the right side of the deque
                deck = deque(f)
                
                # pop stack until a valid page number line
                while True:
                    last_line = deck.pop()
                    if '#' not in last_line:
                        break
                            
                match = pages_lst_format.search(last_line)

                # extract the page number of the last
                if match:
                    number_of_pages = match.group(1)
                
                page_info["number_of_pages"] = int(number_of_pages)
                self.pages[0] = page_info

        except (IOError, IndexError, UnboundLocalError):
            print "Could not open Pages.lst"
       
        #
        # search for page anchors in text 
        # FORMAT: <p id="page%d">
        #
        all_html_files = self.file_operations.list_files(self.working_path, "*.html")
        
        # search for page number anchor in text files
        page_number = 1
        while page_number < int(number_of_pages):
            page_number_info = [None, None]
            
            # FORMAT
            #  <p id="page8">
            anchor_format = re.compile(ur"<p id=\"page%d\">"%page_number)
            # search all content files for anchor
            for filename in all_html_files:
                try:
                    f = codecs.open(filename, "r", encoding='utf-8')
                    file_content = f.read()

                    # search for anchor format
                    match = anchor_format.search(file_content)
                    
                    if match:
                        page_number_info[0] = ("text/" + os.path.basename(filename))
                        page_anchors[page_number] = page_number_info
                        break

                except IOError:
                    print "[ERROR] Could not find page anchors"
                    
                finally:
                    f.close()

            # increment to next page
            page_number += 1
        
        #
        # check for adjusted page number in Pages.lst
        #
        try:
            with codecs.open(self.pages_lst_path, "r", encoding="utf-8") as f:
                start_pos = f.tell()

                for page_number in page_anchors.keys():
                    pages_lst_format = re.compile(ur"^(0{0,3}%d)\|([\d+]+)\s?$"%page_number)
                    for line in f:
                        match = pages_lst_format.search(line)
                        if match:
                            page_anchors[page_number][1] = int(match.group(2))
                            # rewind file
                            f.seek(start_pos)
                            break
        except (IOError, IndexError, UnboundLocalError):
            print "Could not open Pages.lst"

        
        # add to pages list
        self.pages[1] = page_anchors

        #print "Parsed pages.lst", self.pages

    # ==========================================================================
    # METHOD:
    #   check_publication()
    # ==========================================================================
    def check_publication(self):
        """
        DESCRIPTION:
            Check publication state.
        PARAMETERS:
            None
        RETURN: 
            ok      boolean     True if publication is ok, False if not.
        """
        return True
    
    


    
    
