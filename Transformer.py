class Transformer:
     def __init__(self, document):
          self.document = document
          self.pageStyles = document.StyleFamilies.getByName("PageStyles")
          self.defaultStyle = self.pageStyles.getByName("Default Style")
     
     def removeHeaderFooter(self):
            # turn off header and footer for all styles
            for i in range(0, self.pageStyles.getCount()):
               pageStyle = self.pageStyles.getByIndex(i)
               if pageStyle.IsPhysical:
                    print ("Hiding Headers/Footers for page style: " + pageStyle.DisplayName)
                    pageStyle.HeaderIsOn = False
                    pageStyle.FooterIsOn = False

            return

     def setPageSize(self, width, height):
            for i in range(0, self.pageStyles.getCount()):
               pageStyle = self.pageStyles.getByIndex(i)
               if pageStyle.IsPhysical:
                    print ("Setting page size for page style: " + pageStyle.DisplayName)                    
                    pageStyle.Width=width * 100 # in 100th mm 
                    pageStyle.Height=height * 100 # in 100th mm
            
            return
          
     def setMargins(self, top, left, bottom, right):            
            for i in range(0, self.pageStyles.getCount()):
               pageStyle = self.pageStyles.getByIndex(i)
               if pageStyle.IsPhysical:
                    print ("Setting page margins for page style: " + pageStyle.DisplayName)
                    pageStyle.TopMargin = top * 100 # in 100th mm 
                    pageStyle.BottomMargin = bottom * 100 # in 100th mm
                    pageStyle.LeftMargin = left * 100 # in 100th mm 
                    pageStyle.RightMargin = right * 100 # in 100th mm 
            
            return
          
     def setFooterHeight(self, height, bodyDistance):            
            for i in range(0, self.pageStyles.getCount()):
               pageStyle = self.pageStyles.getByIndex(i)
               if pageStyle.IsPhysical:
                    print ("Setting page footer height for page style: " + pageStyle.DisplayName)
                    pageStyle.FooterIsOn = True
                    pageStyle.FooterHeight = height * 100 # in 100th mm (1cm)
                    pageStyle.FooterBodyDistance = bodyDistance * 100  # in 100th mm (1cm)
                    pageStyle.FooterDynamicSpacing = False
                    pageStyle.FooterIsDynamicHeight = False
                    pageStyle.FooterIsOn = False

            return

     def lineNumbering(self, on):
          print ("Setting Line Numbering for document")
          self.document.LineNumberingProperties.IsOn = True
          
          # make sure we're always consistent with the numbering
          self.document.LineNumberingProperties.Interval = 1
          self.document.LineNumberingProperties.CountEmptyLines = False
          self.document.LineNumberingProperties.NumberPosition = 0 # left
          self.document.LineNumberingProperties.NumberingType = 4 # arabic
          self.document.LineNumberingProperties.RestartAtEachPage = False
          return
     
     def removeHeaderFooterLineNumbering(self):
            print ("Removing Header and Footer line numbering")
            paragraphStyles = self.document.StyleFamilies.getByName("ParagraphStyles")
            footer = paragraphStyles.getByName("Footer")
            footer.ParaLineNumberCount = False
            footer = paragraphStyles.getByName("Footer Left")
            footer.ParaLineNumberCount = False
            footer = paragraphStyles.getByName("Footer Right")
            footer.ParaLineNumberCount = False
            header = paragraphStyles.getByName("Header")
            header.ParaLineNumberCount = False
            header = paragraphStyles.getByName("Header Left")
            header.ParaLineNumberCount = False
            header = paragraphStyles.getByName("Header Right")
            header.ParaLineNumberCount = False

            return
     
     def addFooterPageNumbering(self, height, bodyDistance):
            pageNumber = self.document.createInstance("com.sun.star.text.textfield.PageNumber")
            # arabic
            pageNumber.NumberingType = 4
            # set to current page
            pageNumber.SubType = 1
            
            # need to set for all page styles
            self.setFooterHeight(height, bodyDistance)

            # footer needs to be on in order to create cursor
            self.defaultStyle.FooterIsOn = True
            
            footerCursor = self.defaultStyle.FooterText.createTextCursor()
            footerCursor.ParaLineNumberCount = False
            footerCursor.ParaAdjust = 3 # CENTER
            
            self.defaultStyle.FooterText.Text.insertTextContent(footerCursor, pageNumber, True)
            return
     
     
     def transform(self):
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/text/textfield/PageNumber.html
            # http://comments.gmane.org/gmane.comp.openoffice.devel.udk/1693
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/style/NumberingType.html#ARABIC

            self.setPageSize(215.9, 279.4) # us letter
            self.setMargins(20, 30, 20, 20)
          
            # make sure line numbering is enabled
            self.lineNumbering(True)
            
            # remove all headers/footers
            self.removeHeaderFooter()
            
            # not necessary at the momemnt, but if we decide to allow headers/footers, we would want to turn off line numbering there
            # self.removeHeaderFooterLineNumbering()
            
            # following is only necessary if we want to add footer page numbers (perhaps should be done in pdftk though)
            #self.addFooterPageNumbering(20, 5)
          
            return
          
     def comments(self):
            # List of Style Families
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/style/StyleFamilies.html
            
            # Style Properties & Methods
            # http://wiki.openoffice.org/wiki/Documentation/DevGuide/Text/Overall_Document_Features#Styles
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/style/Style.html#ParaStyleConditions
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/container/XIndexAccess.html
            
            # Page Properties
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/style/PageProperties.html
            
            # Paragraph Properties
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/style/ParagraphProperties.html
            
            # Cursor methods
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/text/XText.html
            
            # Document properties
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/text/module-ix.html
            
            # Line Numbering properties
            # http://www.openoffice.org/api/docs/common/ref/com/sun/star/text/LineNumberingProperties.html
            
            return
          
