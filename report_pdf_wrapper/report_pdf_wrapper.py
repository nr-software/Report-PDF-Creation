import fitz
from fitz import Point
from fitz.utils import getColor

'''
This class is used to create a generic PDF report, with customizable widgets, that allow for easy modification and use. 
The code is not pretty, nor is it meant to be, but it gets the job done. 

author: Alex Nuccio (Nuccio & Reidy Software Services LLC)
'''


class PdfWrapper:

    def __init__(self, logo_path=None, document=None, draw_dimensions=False):
        if document is not None:
            # use existing document and create new page on that
            self.document = document
        else:
            # create new document
            self.document = fitz.open()
        self.page = self.document.new_page()
        self.logo_path = logo_path
        if draw_dimensions:
            self.draw_dimensions()

    def draw_report_pdf(self, page_num=None):
        if self.logo_path is not None:
            self.draw_logo(self.logo_path)
        # if document is multiple pages, then add suffix to mutable widget keys to prevent duplication
        if page_num is not None:
            widget_suffix = f"_{page_num}"
        else:
            widget_suffix = ""
        self.draw_technician_info()
        self.draw_customer_info()
        self.draw_equipment_info(widget_suffix)
        self.draw_checklist(widget_suffix)
        self.draw_comments(widget_suffix)

    def draw_service_call_pdf(self):
        if self.logo_path is not None:
            self.draw_logo(self.logo_path)
        self.draw_technician_info()
        self.draw_customer_info()
        self.draw_equipment_info()
        self.draw_work_summary()
        self.draw_materials()

    def save(self, path):
        self.document.save(path)

    def close(self):
        self.document.close()

    def draw_logo(self, logo_path):
        rect = fitz.Rect(60, 0, 260, 200)
        img = open(logo_path, "rb").read()
        self.page.insert_image(rect, stream=img)

    def draw_technician_info(self):
        self.draw_box(Point(300, 48), Point(520, 48), Point(520, 150), Point(300, 150))
        label_to_name = [{"label": "Date:", "field_name": "date_field", "width": 40},
                         {"label": "Technician:", "field_name": "technician_name_field", "width": 60},
                         {"label": "Technician Phone:", "field_name": "technician_phone_field", "width": 100},
                         {"label": "Job #:", "field_name": "job_number_field", "width": 40}]
        height = 25
        start_point = Point(305, 52)
        max_x = 515
        for label in label_to_name:
            width = label['width']
            top_left = start_point
            bottom_right = Point(start_point.x + width, start_point.y + height)
            adjust = self.page.insert_textbox(fitz.Rect(top_left, bottom_right), label['label'], fontsize=11)
            field = fitz.Widget()
            field.field_name = label['field_name']
            field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            field.text_fontsize = 11
            # x0, y0, x1, y1 (top left, top right, bottom left, bottom right)
            field_x = top_left.x + width + 5
            field.rect = fitz.Rect(field_x, top_left.y, max_x, top_left.y + height - adjust)
            self.draw_underline(field.rect)
            self.page.add_widget(field)
            start_point = Point(top_left.x, top_left.y + height)  # update start point for next label

    def draw_customer_info(self):
        self.page.insert_text(Point(62, 171), "Customer Info", fontsize=12)
        label_to_name = [{"label": "Name:", "field_name": "customer_name_field"},
                         {"label": "Address:", "field_name": "customer_address_field"},
                         {"label": "Email:", "field_name": "customer_email_field"},
                         {"label": "Phone:", "field_name": "customer_phone_field"}]
        height = 25
        width = 50
        start_point = Point(70, 180)
        for label in label_to_name:
            top_left = start_point
            bottom_right = Point(start_point.x + width, start_point.y + height)
            adjust = self.page.insert_textbox(fitz.Rect(top_left, bottom_right), label['label'], fontsize=11)
            # Add form fields for name
            field = fitz.Widget()
            field.field_name = label['field_name']
            field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            field.text_fontsize = 11
            # field.field_value = "John Doe"
            # x0, y0, x1, y1 (top left, top right, bottom left, bottom right)
            field_x = top_left.x + width + 5
            field.rect = fitz.Rect(field_x, top_left.y, field_x + 390, top_left.y + height - adjust)
            self.draw_underline(field.rect)
            self.page.add_widget(field)
            start_point = Point(top_left.x, top_left.y + height)  # update start point for next label
        self.draw_box(Point(60, 175), Point(520, 175), Point(520, 277), Point(60, 277))

    def draw_equipment_info(self, widget_suffix=""):
        self.page.insert_text(Point(62, 306), "Equipment Info", fontsize=12)
        self.draw_box(Point(60, 310), Point(520, 310), Point(520, 403), Point(60, 403))
        self.page.insert_text(Point(70, 330), "Make:", fontsize=11)
        self._add_text_widget(f"equipment_make_field{widget_suffix}", Point(70, 314), 25, 170)
        self.page.insert_text(Point(70, 360), "Model:", fontsize=11)
        self._add_text_widget(f"equipment_model_field{widget_suffix}", Point(70, 344), 25, 170)
        self.page.insert_text(Point(300, 330), "Site ID:", fontsize=11)
        self._add_text_widget(f"equipment_site_field{widget_suffix}", Point(300, 314), 25, 160)
        self.page.insert_text(Point(300, 360), "Equipment ID:", fontsize=11)
        self._add_text_widget(f"equipment_id_field{widget_suffix}", Point(320, 344), 25, 140)
        self.page.insert_text(Point(70, 390), "Notes:", fontsize=11)
        self._add_text_widget(f"equipment_notes_field{widget_suffix}", Point(70, 374), 25, 390)

    def _add_text_widget(self, name, top_left, height, width):
        field = fitz.Widget()
        field.field_name = name
        field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        field.text_fontsize = 11
        field.rect = fitz.Rect(top_left.x + 50, top_left.y, top_left.x + 50 + width, top_left.y + height)
        self.draw_underline(field.rect)
        self.page.add_widget(field)

    def draw_checklist(self, widget_suffix=""):
        self.page.insert_text(Point(62, 431), "Inspection Checklist: ", fontsize=12)
        field = fitz.Widget()
        field.field_name = "report_type_field"
        field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        field.text_fontsize = 11
        field.rect = fitz.Rect(175, 415, 300, 435)
        self.page.add_widget(field)
        self.page.insert_text(Point(180, 452), "Task", fontsize=11)
        self.page.insert_text(Point(362, 452), "Completed", fontsize=11)
        self.page.insert_text(Point(435, 452), "Needs attention", fontsize=11, color=getColor("red"))
        self.draw_box(Point(60, 435), Point(520, 435), Point(520, 700), Point(60, 700))
        self.draw_line(Point(60, 460), Point(520, 460))  # title separator
        self.draw_line(Point(350, 435), Point(350, 700))  # middle separator
        self.draw_line(Point(430, 435), Point(430, 700))  # right separator
        # draw checkboxes
        line = 1
        for i in range(463, 700, 15):
            # add completed checkbox
            point = Point(385, i)
            field_name = f"completed_{line}_field{widget_suffix}"
            self._add_checkbox_widget(point, field_name, (0, 0, 0))
            # add line item
            field = fitz.Widget()
            field.field_name = f"task_{line}_field"
            field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            field.text_maxlen = 100
            field.field_flags |= fitz.PDF_FIELD_IS_READ_ONLY
            field.rect = fitz.Rect(68, point.y - 2, 340, point.y + 10)
            self.draw_line(Point(60, i - 3), Point(520, i - 3))
            self.page.add_widget(field)
            # add red attention checkbox
            attention_point = Point(470, i)
            field_name = f"attention_{line}_field{widget_suffix}"
            self._add_checkbox_widget(attention_point, field_name, getColor("red"))
            line += 1

    def _add_checkbox_widget(self, top_left, name, color):
        field = fitz.Widget()
        field.field_name = name
        field.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
        field.border_color = color
        field.border_width = 1
        field.rect = fitz.Rect(top_left, top_left.x + 10, top_left.y + 10)
        self.page.add_widget(field)

    def draw_comments(self, widget_suffix=""):
        self.page.insert_text(Point(62, 726), "Comments", fontsize=12)
        self.draw_box(Point(60, 730), Point(520, 730), Point(520, 810), Point(60, 810))
        field = fitz.Widget()
        field.field_name = f"comments_field{widget_suffix}"
        field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        field.text_fontsize = 11
        field.text_maxlen = 450
        field.rect = fitz.Rect(Point(60, 730), Point(520, 810))
        self.page.add_widget(field)

    def draw_work_summary(self):
        self.page.insert_text(Point(62, 431), "Work Summary", fontsize=12)
        self.draw_box(Point(60, 435), Point(520, 435), Point(520, 550), Point(60, 550))
        field = fitz.Widget()
        field.field_name = "work_summary_field"
        field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        field.text_fontsize = 11
        field.text_maxlen = 450
        field.rect = fitz.Rect(Point(60, 435), Point(520, 550))
        self.page.add_widget(field)

    def draw_materials(self):
        self.page.insert_text(Point(62, 580), "Materials/Parts", fontsize=12)
        self.draw_box(Point(60, 584), Point(520, 584), Point(520, 810), Point(60, 810))
        self.page.insert_text(Point(150, 601), "Item", fontsize=11)
        self.page.insert_text(Point(300, 601), "Qty", fontsize=11)
        self.page.insert_text(Point(400, 601), "Completed?", fontsize=11)
        self.draw_line(Point(60, 609), Point(520, 609))  # title separator
        self.draw_line(Point(275, 584), Point(275, 810))  # middle separator
        self.draw_line(Point(340, 584), Point(340, 810))  # right separator
        # draw checkboxes
        line = 1
        for i in range(612, 800, 20):
            point = Point(385, i)
            # add material item
            field = fitz.Widget()
            field.field_name = f"material_{line}_field"
            field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            field.text_maxlen = 100
            field.rect = fitz.Rect(68, point.y - 2, 275, point.y + 15)
            self.draw_line(Point(60, i - 3), Point(520, i - 3))
            self.page.add_widget(field)
            # add quantity item
            field = fitz.Widget()
            field.field_name = f"quantity_{line}_field"
            field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            field.text_maxlen = 10
            field.rect = fitz.Rect(280, point.y - 2, 330, point.y + 15)
            self.page.add_widget(field)
            self.page.insert_text(Point(350, point.y + 10), "Yes", fontsize=10)
            self._add_checkbox_widget(Point(375, point.y + 2), f"completed_{line}_checkbox", (0, 0, 0))
            self.page.insert_text(Point(430, point.y + 10), "More service", fontsize=10, color=getColor("red"))
            self._add_checkbox_widget(Point(500, point.y + 2), f"service_{line}_checkbox", getColor("red"))

            line += 1

    def draw_underline(self, rect):
        start = (rect.x0, rect.y1)
        end = (rect.x1, rect.y1)
        self.page.draw_line(start, end, color=getColor("black"), width=1)

    def draw_box(self, p1, p2, p3, p4):
        # draw line from p1 -> p2, p2 -> p3, p3 -> p4, p4 -> p1
        top_left = (p1.x, p1.y)
        top_right = (p2.x, p2.y)
        bottom_right = (p3.x, p3.y)
        bottom_left = (p4.x, p4.y)
        self.page.draw_line(top_left, top_right, color=getColor("black"), width=1)
        self.page.draw_line(top_right, bottom_right, color=getColor("black"), width=1)
        self.page.draw_line(bottom_right, bottom_left, color=getColor("black"), width=1)
        self.page.draw_line(bottom_left, top_left, color=getColor("black"), width=1)

    def draw_line(self, p1, p2):
        self.page.draw_line(p1, p2, color=getColor("black"), width=1)

    # -------- for testing ------------
    def draw_dimensions(self):
        print(f"page height: {self.page.rect.height}")
        print(f"page width: {self.page.rect.width}")
        for i in range(50, int(self.page.rect.height), 50):
            self.page.insert_text((1, i), f"{i}", fontsize=8)
            start = (0, i)
            end = (self.page.rect.width, i)
            self.page.draw_line(start, end, color=(235 / 255, 235 / 255, 235 / 255), width=1)
        for i in range(0, int(self.page.rect.width), 50):
            self.page.insert_text((i, 7), f"{i}", fontsize=8)
            start = (i, 0)
            end = (i, self.page.rect.height)
            self.page.draw_line(start, end, color=(235 / 255, 235 / 255, 235 / 255), width=1)

