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
from lxml import etree as etree
from lxml.html import clean as clean

# ==========================================================================
# CLASS:
#   XMLOperations
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class XMLOperations(object):
    """
    DESCRIPTION:

    PARAMETERS:
    """


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(self)
    # ==========================================================================
    def __init__(self):
        pass
        
   
    
    # ==========================================================================
    # METHOD:
    #   build_xhtml_skel_final(title_text, css)
    # ==========================================================================
    def build_xhtml_skel_final(self, title_text, css):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        
        
        #
        # <html>
        #
        HTML_NSMAP =    {   None    :   "http://www.w3.org/1999/xhtml" }
        root = etree.Element("html", nsmap=HTML_NSMAP)
        tree = etree.ElementTree(root)
        
        #
        # <head>
        #
        head = etree.Element("head")
        root.append(head)

        # meta (encoding)
        attrib = {  "http-equiv":   "content-type",  
                    "content"   :   "application/xhtml+xml; charset=utf-8" }
        meta = etree.Element("meta", attrib)
        head.append(meta)

        # title
        title = etree.Element("title")
        title.text = title_text
        head.append(title)

        # css
        attrib = { "rel": "stylesheet", "type":"text/css", "href":css}
        css_link = etree.Element("link", attrib)
        head.append(css_link)


        return tree
    
    # ==========================================================================
    # METHOD:
    #   build_table_skel(body, table_name, header)
    # ==========================================================================
    def build_table_skel(self, body, table_name, header):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        h3 = etree.Element("h3")
        h3.text = table_name
        body.append(h3)
        
        # table
        attribs = { "class" : "table_report" }
        table = etree.Element("table", attribs)
        body.append(table)
        
        # theader
        thead = etree.Element("thead")
        table.append(thead)
        tr  = etree.Element("tr")
        thead.append(tr)
        for entry in header:
            attrib = { "scope" : "col"}
            th = etree.Element("th", attrib)
            th.text = entry
            tr.append(th)

        # tbody
        tbody = etree.Element("tbody")
        table.append(tbody)

        return tbody

    # ==========================================================================
    # METHOD:
    #   build_table_final_objects(body, table_name, header, report_entries)
    # ==========================================================================
    def build_table_final_objects(self, body, table_name, header, report_entries):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        h3 = etree.Element("h3")
        h3.text = table_name
        body.append(h3)


        # table
        attribs = { "class" : "table_report" }
        table = etree.Element("table", attribs)
        body.append(table)
        
        # theader
        thead = etree.Element("thead")
        table.append(thead)
        tr  = etree.Element("tr")
        thead.append(tr)
        for entry in header:
            attrib = { "scope" : "col"}
            th = etree.Element("th", attrib)
            th.text = entry
            tr.append(th)

        # tbody
        tbody = etree.Element("tbody")
        table.append(tbody)
        for entry in report_entries:
            entry_type = entry.get_type()
            filename = entry.get_filename()
            encoding = entry.get_encoding()
            markup_status = entry.get_markup_status()
            spellcheck_status = entry.get_spellcheck_status()


            tr = etree.Element("tr")
            tbody.append(tr)
            
            # filename
            td = etree.Element("td")
            td.text = os.path.basename(filename)
            tr.append(td)

            # encoding
            attrib = { "class" : encoding["status"]}
            td = etree.Element("td", attrib)
            td.text = encoding["encoding"]
            tr.append(td)

            #
            # publication content
            #
            
            if entry_type is "content":
                # markup
                markup_errors = len(markup_status["errors"])
                
                if markup_errors > 0:
                    attrib = { "class" : markup_status["status"], "href" : markup_status["details"]}
                    td = etree.Element("td")
                    tr.append(td)
                    a = etree.Element("a", attrib)
                    a.text = str(markup_errors)
                    td.append(a) 
                else:
                    attrib = { "class" : markup_status["status"]}
                    td = etree.Element("td", attrib)
                    td.text = str(markup_errors)
                    tr.append(td)
                    

                # spellcheck
                # spellcheck errors occured and details created
                if len(spellcheck_status["errors"]) > 0 and spellcheck_status["details"] is not None:
                    attrib = { "class" : spellcheck_status["status"], "href" : spellcheck_status["details"]}
                    td = etree.Element("td")
                    tr.append(td)
                    a = etree.Element("a", attrib)
                    a.text = str(len(spellcheck_status["errors"]))
                    td.append(a) 
                # markup error prevented spellchecker from running
                elif spellcheck_status["status"] == "N/A":
                    td = etree.Element("td")
                    td.text = str(spellcheck_status["status"])
                    tr.append(td)
                # no spelling spelling errors found
                else:
                    attrib = { "class" : spellcheck_status["status"]}
                    td = etree.Element("td", attrib)
                    td.text = str(len(spellcheck_status["errors"]))
                    tr.append(td)

                

            # articles 
            if entry_type is "articles":
                articles_status = entry.get_articles_status()
                
                attrib = { "class" : articles_status["parsable"]}
                td = etree.Element("td", attrib)
                td.text = articles_status["parsable"]
                tr.append(td)

                attrib = { "class" : articles_status["status"], "href" : articles_status["details"]}
                td = etree.Element("td")
                tr.append(td)
                a = etree.Element("a", attrib)
                a.text = "View report"
                td.append(a) 
            
            # metadata
            if entry_type is "metadata":
                metadata_status = entry.get_metadata_status()
                
                attrib = { "class" : metadata_status["parsable"]}
                td = etree.Element("td", attrib)
                td.text = metadata_status["parsable"]
                tr.append(td)

                attrib = { "class" : metadata_status["status"], "href" : metadata_status["details"]}
                td = etree.Element("td")
                tr.append(td)
                a = etree.Element("a", attrib)
                a.text = "View report"
                td.append(a) 




    # ==========================================================================
    # METHOD:
    #   build_content_opf_skel_final():
    # ==========================================================================
    def build_content_opf_skel_final(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        
        #
        # <package>
        #
        #PACKAGE_NSMAP = {   None    :   "http://www.idpf.org/2007/opf/" }
      
        #
        # NOTE: register namespace as attrib instead of nsmap because of
        # duplication in META_NSMAP
        attribs =       {    "xmlns"  :     "http://www.idpf.org/2007/opf",
                            "unique-identifier" : "BookId",
                            "version"           : "2.0" }

        #root = etree.Element("package", attribs, nsmap=PACKAGE_NSMAP)
        root = etree.Element("package", attribs)
        tree = etree.ElementTree(root)
        

        #
        # <metadata>
        #
        META_NSMAP =    {   "opf"   :   "http://www.idpf.org/2007/opf",
                            "dc"    :   "http://purl.org/dc/elements/1.1/"
                        }

        metadata = etree.Element("metadata", nsmap = META_NSMAP)
        root.append(metadata)


        #
        # <manifest>
        #
        manifest = etree.Element("manifest")
        root.append(manifest)
        
        #
        # <spine>
        #
        attribs_spine =    {   "toc"    :   "ncx" }
        spine = etree.Element("spine", attribs_spine)
        root.append(spine)
        
        #
        # <guide>
        #
        guide = etree.Element("guide")
        root.append(guide)
        
        return tree


    # ==========================================================================
    # METHOD:
    #   build_ncx_skel_final()
    # ==========================================================================
    def build_ncx_skel_final(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        #
        # <ncx>
        #
        NCX_NSMAP =     {   None    :   "http://www.daisy.org/z3986/2005/ncx/" }
        attribs =       {   "version"           : "2005-1"  }

        root = etree.Element("ncx", attribs, nsmap=NCX_NSMAP)
        tree = etree.ElementTree(root)

        head = etree.Element("head")
        root.append(head)

        return tree



    # ==========================================================================
    # METHOD:
    #   insert_paragrap_into_XHTML_final(tree, page_number, text)
    # ==========================================================================
    def insert_paragrap_into_XHTML_final(self, tree, page_number, text):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        
        root = tree.getroot()

        #
        # build 
        # 
        body = root.find("body")
        
        if body is None:
            body = etree.Element("body")
            root.append(body)


        #
        # insert text into a single paragraph
        #
        attribs = { "id" : "page" + str(page_number) }
        p = etree.Element("p", attribs)
        p.text = text
        body.append(p)


    # ==========================================================================
    # METHOD:
    #   replace_attrib(self,tree, element_tag, attrib, value)
    # ==========================================================================
    def replace_attrib(self, tree, element_tag, attrib, value):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        

        # search for attribute
        for element in tree.getiterator():
            if element.tag == element_tag:
                element.attrib[attrib] = value
                


    # ==========================================================================
    # METHOD:
    #   clean_markup(tree)
    # ==========================================================================
    def clean_markup(self, tree):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        # clean up tree 
        cleaner = clean.Cleaner(allow_tags=['table', 'tr', 'td', 'h3'],
                remove_unknown_tags=False, safe_attrs_only=True)
        cleaner.clean_html(tree)

        return tree

