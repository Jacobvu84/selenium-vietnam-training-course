__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage
from scenarios.resource import user_dir
from scenarios.util.support import TARGET

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class DocumentPage(BasePage):
    up_file = (By.LINK_TEXT, 'Upload File')
    col_xpath = "//table[@id='fileListTable']/tbody/tr[1]/td[" \
                "count(//table[@id='fileListTable']/thead/tr/th[text()='{0}']/preceding-sibling::*) + 1]"

    def get_text_by_col_name(self, name):
        domain_col = (By.XPATH, self.col_xpath.format(name))
        return self.element(*domain_col).get_text_value()

    @Test()
    def select_file_to_upload(self, path_file):
        path_pic = user_dir + "\\images\\" + path_file
        self.element(*self.up_file).click_and_wait()
        self.upload_file(path_pic)
        return self

    @Test()
    def get_doc_description(self):
        return self.get_text_by_col_name("Description")

    def get_table_empty(self):
        table_empty = (By.XPATH, "//table[@id='fileListTable']//td[@class='dataTables_empty']")
        return self.element(*table_empty).get_text_value()

    @Test(("Undefined", "Undefined"))
    def get_image_resource(self, file='my_doc.png'):
        path_pic = user_dir + "\\images\\" + file
        return path_pic

    def click_on_view(self):
        view_doc = (By.XPATH, '//a[@data-action="File.open"]')
        self.element(*view_doc).click_and_wait()
        return self

    @Test(("Undefined", "Undefined"))
    def capture_document_image(self, image_name):
        docu = (By.XPATH, '//img')
        self\
            .switch_to_new_window()\
            .element(*docu)\
            .capture_element(image_name)\
            .close_active_window()\
            .switch_default_window()
        return TARGET + image_name + '.png'

    def click_on_delete(self, msg):
        del_file = (By.XPATH, '//a[@data-action="File.simpleremove"]')
        self.element(*del_file).click_and_wait().accept_alert(alert_text=msg)
        return self

