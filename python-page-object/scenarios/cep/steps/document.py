__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.document import DocumentPage
from util.assertions import Assert


class DocumentSteps(Assert):
    on_doc_page = DocumentPage()

    def upload_document(self, file_name):
        self\
            .on_doc_page\
            .select_file_to_upload(file_name)
        return self

    def should_see_the_document(self, docs):
        self.verifyEquals(self.on_doc_page.get_doc_description(), docs)
        return self

    def should_see_the_message(self, msg):
        self.verifyEquals(self.on_doc_page.get_table_empty(), msg)
        return self

    def view_document(self, value):
        image_res = self.on_doc_page.get_image_resource()
        self.on_doc_page.click_on_view()
        image_des = self.on_doc_page.capture_document_image(value)
        self.compare_image_by_rgba(image_res, image_des)
        return self

    def delete_document(self, msg):
        self.on_doc_page.click_on_delete(msg)
        return self



