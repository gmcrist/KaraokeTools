#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class Canvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

        self._currentHeaderText = ''
        self._currentFooterText = ''

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        self._pageCount = len(self._saved_page_states)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.drawPageContent()
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    def drawPageContent(self):
        # Header
        self.setFont('Helvetica-Bold', 18)
        self.drawCentredString(4.25*inch, 10.25*inch, self._currentHeaderText)

        # Footer
        self.setFont('Helvetica', 8)
        self.setLineWidth(0.25)

        if (self._pageNumber % 2 == 0):
            # Even pages
            self.line(0.25*inch, 0.40*inch, 7.50*inch, 0.40*inch)

            self.drawRightString(7.50*inch, 0.25*inch, self._currentFooterText)

            self.drawString(0.25*inch, 0.25*inch,
                'Page {} of {}'.format(self._pageNumber, self._pageCount))
        else:
            # Odd pages
            self.line(1.00*inch, 0.40*inch, 8.25*inch, 0.40*inch)

            self.drawString(1.00*inch, 0.25*inch, self._currentFooterText)
            self.drawRightString(8.25*inch, 0.25*inch,
                'Page {} of {}'.format(self._pageNumber, self._pageCount))
