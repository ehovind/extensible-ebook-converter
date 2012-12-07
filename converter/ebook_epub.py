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
import ImageFont, ImageDraw, Image

from lxml import etree as etree

import xml.etree.ElementTree as ET

from converter.ebook_factory import EbookFactory

# ==========================================================================
# CLASS:
#   EbookEpub(EbookFactory)
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class EbookEpub(EbookFactory):
    """
    DESCRIPTION:
    
    PARAMETERS:
    """
    
    ebook_format = "epub"
    container_template_path = "converter/templates/ebook_containers/epub2/"
    book_css = "../css/book.css"

    # recommended cover size (RESEARCH)
    cover_size = 600, 800



    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(path_info, ebook_source)
    # ==========================================================================
    def __init__(self, path_info, ebook_source):
        EbookFactory.__init__(self, path_info, ebook_source)

        # get all article info
        self.articles = self.ebook_source.get_articles()
        
        # get metadata info
        self.metadata = self.ebook_source.get_metadata()
        
        # get pages info
        self.pages = self.ebook_source.get_pages()
        
        # workspace path info
        self.title = ebook_source.get_title()
        self.output_path =  path_info["output_path"] + "/epub"  # no trail backlash
        self.output_ebook_file = "../" + self.title + ".epub"
        self.content_opf = self.output_path + "/OEBPS/content.opf" 
        self.toc_ncx = self.output_path +  "/OEBPS/toc.ncx" 
        self.toc_html_path = self.output_path + "/OEBPS/text/toc.html"
        self.preface_xhtml_path = self.output_path + "/OEBPS/text/preface.html" 
        self.colophon_xhtml_path = self.output_path + "/OEBPS/text/colophon.html" 
        self.epub_text_path =  self.output_path + "/OEBPS/text/"
        self.images_path =  self.output_path + "/OEBPS/images/"
        self.style_path =  self.output_path + "/OEBPS/css/"
        self.cover_xml = self.output_path +  "/OEBPS/cover.xml" 
        self.cover_path =  self.output_path + "/OEBPS/images/" + self.cover_gif
        self.cover_user_provided_path =  self.working_path + "/images/" + self.cover_gif
        self.toc_text = "Innhald"
        self.preface_text = "Forord"
        self.colophon_text = "Kolofon"
        
        



    # ==========================================================================
    # METHOD:
    #   build()
    # ==========================================================================
    def build(self):
        """
        DESCRIPTION:
            Build an ebook publication.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "[STATUS] Building epub... "

        # validate input source
        try:
            if not self.validate_source():
                print "[FATAL] Input content is not XHTML, exiting..."
                sys.exit(1)
        except NotImplementedError:
            print "[FATAL] source validator not implemented"
            sys.exit(1)

        

        # prepare epub container skel
        self.prepare_container()


        # update publication content
        self.update_publication_content()


        #  build parts of ebook
        # self.build_preface_xhtml()
        self.build_colophon_xhtml()
        self.build_cover()
        self.create_toc_html()
       

        # content.opf
        self.create_content_opf()
        self.create_toc_ncx()

      


    # ==========================================================================
    # METHOD:
    #   prepare_container()
    # ==========================================================================
    def prepare_container(self):
        """
        DESCRIPTION:
            Prepare container. Copy template from resources.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] prepare container... "

        # copy container skeleton
        try:
            shutil.copytree(EbookEpub.container_template_path, self.output_path, 
                        ignore=shutil.ignore_patterns('*.svn*'))
        except OSError:
            print "\t\tcontainer already present, copy not needed"

        # explicit copy of cover template
        template_cover =  EbookEpub.container_template_path + "/OEBPS/images/" + self.cover_gif
        container_cover =  self.output_path + "/OEBPS/images/" + self.cover_gif
        shutil.copy2(template_cover, container_cover)


    # ==========================================================================
    # METHOD:
    #   update_publication_content()
    # ==========================================================================
    def update_publication_content(self):
        """
        DESCRIPTION:
            Update the publication content.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        
        # update the container text
        self.update_container_text()

        # update the container text
        self.update_container_images()
        
        # update container style
        self.update_container_style()
        

    # ==========================================================================
    # METHOD:
    #    update_container_text()
    # ==========================================================================
    def update_container_text(self):
        """
        DESCRIPTION:
            Update publication text. Modify css and images location relative
            to ePub container structure.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Update container text... "

        # create empty folder
        try:
            os.mkdir(self.epub_text_path)
        except OSError:
            pass
        
        # copy source files
        all_html_files = self.file_operations.list_files(self.working_path, "*.html")
        
        for filename in all_html_files:
            shutil.copy2(filename, self.epub_text_path)

            # modify css and images location
            parser = etree.XMLParser()
            tree = etree.parse(filename, parser)
            self.xml_operations.replace_attrib(tree,
                    "{http://www.w3.org/1999/xhtml}link",
                                                      "href", self.book_css    ) 
            self.xml_operations.replace_attrib(tree,
                    "{http://www.w3.org/1999/xhtml}img",
                                                      "src", "../images/"    ) 
            # serialize the XML to Unicode strings
            root_unicode = etree.tostring(tree.getroot(), encoding=unicode, pretty_print=True)
        
            # write xml tree to file
            filename_only = self.file_operations.filename_only_final(filename)
            epub_text_file = self.epub_text_path + filename_only
            self.file_operations.write_xml(epub_text_file, root_unicode)
                                                   




    # ==========================================================================
    # METHOD:
    #   update_container_images()
    # ==========================================================================
    def update_container_images(self):
        """
        DESCRIPTION:
            Update images from working directory. 
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Update container images... "
        
        # copy all image files
        all_image_files = self.file_operations.list_files(self.working_path + "/images/", "*.*")
        
        for filename in all_image_files:
            shutil.copy2(filename, self.images_path)

    # ==========================================================================
    # METHOD:
    #   update_container_style()
    # ==========================================================================
    def update_container_style(self):
        """
        DESCRIPTION:
            Update css from working directory.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Update container style... "
        
        # create empty folder
        try:
            os.mkdir(self.style_path)
        except OSError:
            pass
        
        # copy all image files
        all_style_files = self.file_operations.list_files(self.working_path + "/css/", "*.css")
        
        for filename in all_style_files:
            shutil.copy2(filename, self.style_path)



    # ==========================================================================
    # METHOD:
    #   create_toc_html(self)
    # ==========================================================================
    def create_toc_html(self):
        """
        DESCRIPTION:
            Create a Table of Contents (toc.html) based on information from
            Articles.lst.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Build toc xhtml... "
        
        # create HTML, TITLE, CSS link, META, body
        tree = self.xml_operations.build_xhtml_skel_final("Innhold", self.book_css)
        
        root = tree.getroot()
        body = etree.Element("body")
        root.append(body)

        h2 = etree.Element("h2")
        h2.text =  "Innhold"
        body.append(h2)
                
        # insert p
        p = etree.Element("p")
        body.append(p)

        # insert a
        for article in self.articles:
            link = etree.Element("a", href=article[1])
            link.text = article[2]
            p.append(link)
            line_break = etree.Element("br")
            p.append(line_break)

        # add to articles after preface
        try:
            index = 0
            for item in self.articles:
                if item[0] is "preface":
                    entry = ["toc", "toc.html", "Innhold", (None, None)]
                    self.articles.insert(index+1, entry)
                    break
                index += 1

        except (ValueError, IndexError) as err:
            print "could not insert articles into toc.html", err


        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)
        
        # write xml tree to file
        self.file_operations.write_xml(self.toc_html_path, root_unicode)

    # ==========================================================================
    # METHOD:
    #   create_toc_html(self)
    # ==========================================================================
    def build_cover(self):
        """
        DESCRIPTION:
            Build a cover. Either from pre-defined cover image, or generated using
            Pythin Imaging Library.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Build cover... "

        author = self.metadata["title"][1]
        title_full = self.metadata["creator"][4][0]
       
        # check for 
        print "\t\tsearching for " + self.cover_gif + "...",
        if os.path.exists(self.cover_user_provided_path):
            print "found."
            
            # checking size
            print "\t\tchecking size...",
            try:
                image = Image.open(self.cover_path)
                dimensions = image.size

                if dimensions[0] is not self.cover_size[0] or dimensions[1] is not self.cover_size[1]:
                    print "\t\t\tresizing cover to ", self.cover_size
                    image = Image.open(self.cover_path)
                    image_resize = image.resize(self.cover_size, Image.ANTIALIAS)
                    image_resize.save(self.cover_path)
            except IOError as ioe:
                print "cannot open image: ", ioe

            print "\n"

        # generating cover from template
        else:
            print "\n\t\t no cover provided, generating from template"
            startx = 0
            starty = 300
            font = None

            # open image and creata a Draw object
            im = Image.open(self.cover_path)
            draw = ImageDraw.Draw(im)
            
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf", 32)
            except IOError as ioe:
                font = ImageFont.load_default()

            # add title text
            text_width, text_height = draw.textsize(title_full, font)
            startx = (self.cover_size[0] - text_width)/2
            draw.text((startx, starty), title_full, font=font, fill=255)

            # add author text
            text_width, text_height = draw.textsize(author, font)
            startx = (self.cover_size[0] - text_width)/2
            starty = starty + (text_height + 100)
            draw.text((startx, starty), author, font=font, fill=255)
            im.save(self.cover_path,"GIF")


        # create HTML, TITLE, CSS link, META, body
        book_css = self.book_css.replace("../","")

        tree = self.xml_operations.build_xhtml_skel_final("Cover", book_css)


        # move to xml_operations, with exception handling
        root = tree.getroot()
        body = etree.Element("body")
        root.append(body)
        
        # insert p
        p = etree.Element("p")
        body.append(p)

        attribs = { "src":"images/cover.gif", "alt":"Cover", "style":"height:800px;width=600px"}
        img = etree.Element("img", attribs)
        p.append(img)

        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)
        
        # write xml tree to file
        self.file_operations.write_unicode_final(self.cover_xml, root_unicode)



    
    
    # ==========================================================================
    # METHOD:
    #   build_colophon_xhtml()
    # ==========================================================================
    def build_colophon_xhtml(self):
        """
        DESCRIPTION:
            Build a colophon with auto-generated text.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Build colophon... ",
        
        # create HTML, TITLE, CSS link, META, body
        tree = self.xml_operations.build_xhtml_skel_final("Colophon", self.book_css)

        # build colophon from template
        root = tree.getroot()
        body = etree.Element("body")
        root.append(body)
        
        h1 = etree.Element("h1")
        h1.text = self.ebook_source.get_title()
        body.append(h1)

        p = etree.Element("p")
        p.text = "Teksten er hentet fra Prosjekt Runeberg."
        body.append(p)

        p = etree.Element("p")
        p.text = "Konvertering til ePub av Extensible eBook Converter (EeCon)."
        body.append(p)


        # add to articles before preface
        try:
            index = 0
            for item in self.articles:
                if item[0] is "preface":
                    entry = ["colophon", "colophon.html", "Kolofon", (None, None)]
                    self.articles.insert(index, entry)
                    break
                index += 1

        except (ValueError, IndexError) as err:
            print "could not insert colophon.html in articles", err
        


        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, encoding=unicode, pretty_print=True)
        
        # write xml tree to file
        self.file_operations.write_unicode_final(self.colophon_xhtml_path, root_unicode)

        print "done."


    # ==========================================================================
    # METHOD:
    #   create_content_opf()
    # ==========================================================================
    def create_content_opf(self):
        """
        DESCRIPTION:
            Create content.opf.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Build content.opf... ",

        # lxml versions older than 2.3 has different syntax for registering a namespace
        if "2.3" in etree.__version__[:3]:
            ET.register_namespace('dc',"http://purl.org/dc/elements/1.1")
            ET.register_namespace('opf',"http://www.idpf.org/2007/opf/")
        else:
            ET._namespace_map["http://purl.org/dc/elements/1.1"] = 'dc'
            ET._namespace_map["http://www.idpf.org/2007/opf/"] = 'opf'

        dc_elements_ns = "{http://purl.org/dc/elements/1.1/}" 
        opf_element_ns = "{http://www.idpf.org/2007/opf}"
            
        media_type = "application/xhtml+xml"

        
        # create content.opf skeleton
        tree = self.xml_operations.build_content_opf_skel_final()
        root = tree.getroot()


        #
        # insert METADATA elemnts
        #
        metadata = root.find('metadata')
        
        # iterate and add all elements
        for key in self.metadata.keys():
            dc_value = self.metadata[key][1]

            # dc element has a value
            if dc_value is not None:
                dc_element = self.metadata[key][0]
                dc_attribute = self.metadata[key][2]
                dc_element_full = dc_elements_ns + dc_element

                opf_attribute = self.metadata[key][6]
                # check for opf attribute
                if opf_attribute is not None:
                    opf_value = self.metadata[key][7]
                    opf_element_full = opf_element_ns + opf_attribute
                    attribs = { opf_element_full : opf_value}
                    
                    # check for dc element attribute
                    if dc_attribute is not None:
                        dc_attribute_value = self.metadata[key][3]
                        attribs[dc_attribute] = dc_attribute_value
                # plain dc element, without attribute or opf
                else:
                    attribs = {}
                
                # check for multiple dc_values in metadata element
                if isinstance(dc_value, list):
                    lookup_values = self.metadata[key][4]
                    # use lookup strings
                    if len(lookup_values) > 0:
                        values = lookup_values
                    # use authorkeys
                    else:
                        values = dc_value
                    # add values in list
                    for val in values:
                        meta = etree.SubElement(metadata, dc_element_full, attribs)
                        meta.text = val
                        metadata.insert(0, meta)
                # string value in metadata element
                else:
                    meta = etree.SubElement(metadata, dc_element_full, attribs)
                    meta.text = dc_value
                    metadata.insert(0, meta)



        #
        # insert MANIFEST elements
        #
        manifest = root.find('manifest')

        # add all articles to manifest 
        for article in self.articles:
            attrib_id = None
            article_filename = article[1]
            
            # article is a chapter
            if "chapter" in article[0]:
                attrib_id = article[0]

            # if article filename is a known publication structure type
            else:
                attrib_id = article[0]
            
            # add manifest item
            attribs = { "href" : "text/" + article_filename, "id" : attrib_id, "media-type" : media_type }
            item = etree.Element("item", attribs)
            manifest.append(item)
                

        # insert CSS elements
        comment = etree.Comment("CSS Style Sheets")
        manifest.append(comment)
        attribs = { "id" : "main-css", "href":"css/book.css", "media-type":"text/css" }
        css = etree.Element("item", attribs)
        manifest.append(css)
        
        #
        # Image
        #
        # insert Cover elements
        comment = etree.Comment("Images")
        manifest.append(comment)
        attribs = { "id" : "cover-image", "href":"images/cover.gif", "media-type":"image/gif" }
        cover = etree.Element("item", attribs)
        manifest.append(cover)
        attribs = { "id" : "cover", "href":"cover.xml", "media-type":"application/xhtml+xml" }
        cover = etree.Element("item", attribs)
        manifest.append(cover)
        # other images
        all_html_files = self.file_operations.list_files(self.epub_text_path, "*.html")
        all_images = self.xml_operations.find_tag(all_html_files, 
                "{http://www.w3.org/1999/xhtml}img", "src")
        for image in all_images:
            if image.endswith("jpg"):
                media_type = "image/jpeg"
            elif image.endswith("gif"):
                media_type = "image/gif"
            else:
                media_type = "image/png"

            image_id = "image" + os.path.splitext(os.path.basename(image))[0]
            image_ref = "images/" + (os.path.basename(image))
            attribs = {"id":image_id, "href":image_ref, "media-type":media_type}
            image_item = etree.Element("item", attribs)
            manifest.append(image_item)

        # insert NCX element
        comment = etree.Comment("NCX")
        attribs = { "id" : "ncx", "href":"toc.ncx", "media-type":"application/x-dtbncx+xml" }
        ncx = etree.Element("item", attribs)
        manifest.append(comment)
        manifest.append(ncx)


        #
        # insert SPINE elements
        #

        spine = root.find('spine')
        # cover
        attribs = { "idref" : "cover", "linear" : "no" }
        item = etree.Element("itemref", attribs)
        spine.append(item)
        
        # add all articles to spine
        for article in self.articles:
            attrib_id = None
            linear = "yes"
            #article_filename = article[1]
            
            # article is a chapter
            if "chapter" in article[0]:
                attrib_id = article[0]

            # if article filename is a known publication structure type
            else:
                attrib_id = article[0]
                linear = "no"
            
            # add manifest item
            attribs = { "idref" : attrib_id, "linear" : linear }
            item = etree.Element("itemref", attribs)
            spine.append(item)


        #
        # insert GUIDE elements
        #
        guide = root.find('guide')
        
        # add TOC reference
        attribs = { "type" : "toc", "title" : "Table of Contents", "href" : "text/toc.html" }
        reference = etree.Element("reference", attribs)
        guide.append(reference)

        




        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, xml_declaration=True, encoding='UTF-8', pretty_print=True)
        
        # write xml tree to file
        self.file_operations.write_xml_new(self.content_opf, root_unicode)
        
        print "done."

    
    # ==========================================================================
    # METHOD:
    #   create_toc_ncx()
    # ==========================================================================
    def create_toc_ncx(self):
        """
        DESCRIPTION:
            Create toc.ncx.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Build toc.ncx... ",
      
        tree = self.xml_operations.build_ncx_skel_final()
        root = tree.getroot()
      
        #
        # <meta>
        # 
        head =  root.find('head')
        attribs = { "name" : "dtb:uid", "content" : "Espen Hovind"}
        #meta = etree.SubElement(head, "meta", attribs)
        etree.SubElement(head, "meta", attribs)


        #
        # Doc info
        #
        doctitle = etree.Element("docTitle")
        title = etree.SubElement(doctitle, "text")
        title.text = "DOC TITLE"
        root.append(doctitle)
        
        docauthor = etree.Element("docAuthor")
        author = etree.SubElement(docauthor, "text")
        author.text = "DOC AUTHOR"
        root.append(docauthor)

        #
        # Nav map
        #
        navmap = etree.Element("navMap")
        root.append(navmap)
        navmap = root.find("navMap")

        play_order = 1

        # add all articles to spine
        for article in self.articles:
            #attrib_id = None
            #linear = "yes"
            
            # article is a chapter
            #if "chapter" in article[0]:
            #    attrib_id = article[0]

            # if article filename is a known publication structure type
            #else:
            #    attrib_id = article[0]
            #    linear = "no"
            
            # add navpoint
            attribs = { "id" : "navpoint-" + str(play_order), "playOrder" : str(play_order) }
            navpoint = etree.SubElement(navmap, "navPoint", attribs)
            navlabel = etree.SubElement(navpoint, "navLabel")
            nav_label_text = etree.SubElement(navlabel, "text")
            nav_label_text.text = article[2]
            attribs = { "src": "text/" + article[1]}
            #nav_content = etree.SubElement(navpoint, "content", attribs)
            etree.SubElement(navpoint, "content", attribs)
            play_order += 1


        #
        # pageList
        #
        # search for page number anchor in text files
        first = True
        page_number = 1
        for page_number in self.pages[1].keys():
            html_file = self.pages[1][page_number][0]
            adjusted_page_number = self.pages[1][page_number][1]

            if adjusted_page_number != 0:
                if first:
                    page_list = etree.Element("pageList")
                    root.append(page_list)
                    first = False

                attribs = { 
                            "id"        : "page" + str(adjusted_page_number),
                            "type"      : "normal",
                            "value"     : str(adjusted_page_number)
                          }
                page_target = etree.SubElement(page_list, "pageTarget", attribs)
                nav_label = etree.SubElement(page_target, "navLabel")
                nav_label_text = etree.SubElement(nav_label, "text")
                nav_label_text.text = str(adjusted_page_number)
                attribs = { "src": html_file +"#page" + str(page_number)}
                #page_list_content = etree.SubElement(page_target, "content", attribs)
                etree.SubElement(page_target, "content", attribs)


        # serialize the XML to Unicode strings
        root_unicode = etree.tostring(root, xml_declaration=True, encoding="UTF-8", pretty_print=True)
        
        # write xml tree to file  (chapter already UTF-8, dont reencode)
        self.file_operations.write_xml_final(self.toc_ncx, root_unicode)

     
        print "done."
   
    # ==========================================================================
    # METHOD:
    #   compress()
    # ==========================================================================
    def compress(self):
        """
        DESCRIPTION:
            Compress container into an ePub according to reference documentation.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Compress epub... ",

        # compress epub
        os.chdir(self.output_path)
        
        # remove old .epub
        try:
            os.remove(self.output_ebook_file)
        except OSError:
            pass

        
        # compress mimetype
        command = "zip -X -0 -r " + self.output_ebook_file + " mimetype" + " -x \*.svn* 1>/dev/null"
        os.system(command)
        
        command = "zip -X -8 -r " + self.output_ebook_file + " META-INF/ OEBPS/" + " -x \*.svn* 1>/dev/null"
        os.system(command)
       
        # change, research stack popd
        os.chdir("../../../../../../../")
        print "done."


    # ==========================================================================
    # METHOD:
    #   validate_source()
    # ==========================================================================
    def validate_source(self):
        """
        DESCRIPTION:
            Validate that input content is XHTML
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "[STATUS] Validating source... "
        all_html_files = self.file_operations.list_files(self.working_path, "*.html")
        
        for filename in all_html_files:
            try:
                parser = etree.XMLParser()
                etree.parse(filename, parser)
    
            except etree.XMLSyntaxError:
                return False
        
        return True
    
    # ==========================================================================
    # METHOD:
    #   validate_ebook()
    # ==========================================================================
    def validate_ebook(self):
        """
        DESCRIPTION:
            Validate ePub using external tool.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        print "\t[STATUS] Validating epub..."

        # validate epub
        #command = "java -jar /home/espen/Desktop/temp_master/epubcheck-3.0b5/epubcheck-3.0b5.jar " + 
        #os.system(command)

