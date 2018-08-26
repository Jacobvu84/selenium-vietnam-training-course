__author__ = 'jacob@vsee.com'

import logging
import math, operator
from PIL import Image

log = logging.getLogger('report')


class Assert(object):
    def verifyEquals(self, expect, actual):
        """The Test will continue executing and logging the failure."""
        if expect == actual:
            log.debug("[TEST PASSED]: '{0}' is equal to '{1}'".format(expect, actual))
            return True
        else:
            log.debug("[TEST FAILED]: '{0}' is not equal to '{1}'".format(expect, actual))
            return False
    def assertEquals(self, expect, actual):
        """The test execution will be aborted"""
        if expect == actual:
            log.debug("[TEST PASSED]: '{0}' is equal to '{1}'".format(expect, actual))
            assert True
        else:
            assert False, log.debug("[TEST FAILED]: '{0}' is not equal to '{1}'".format(expect, actual))

    def verifyContainsString(self, subString, supString):
        if subString in supString:
            log.debug("[TEST PASSED]: '{0}' is in '{1}'".format(subString, supString))
            return True
        else:
            return False, log.debug("[TEST FAILED]: '{0}' not contains '{1}'".format(supString, subString))

    def assertContainsString(self, subString, supString):
        """The test execution will be aborted"""
        if subString in supString:
            log.debug("[TEST PASSED]: '{0}' is in '{1}'".format(subString, supString))
            assert True
        else:
            assert False, log.debug("[TEST FAILED]: '{0}' not contains '{1}'".format(supString, subString))

    def assertNotContainsString(self, subString, supString):
        """The test execution will be aborted"""
        if subString not in supString:
            log.debug("[TEST PASSED]: '{0}' is not in '{1}'".format(subString, supString))
            assert True
        else:
            assert False, log.debug("[TEST FAILED]: '{0}' contains '{1}'".format(supString, subString))

    def compare_image_by_rgba(self, res, des):
        im1 = Image.open(res)
        im2 = Image.open(des)
        width1, height1 = im1.size
        width2, height2 = im2.size
        if width1 != width2 or height1 != height2:
            log.debug("[TEST FAILED]: {0} size is not the same {1} size".format(im1.size, im2.size))
            return False
        else:
            px1 = im1.load()
            px2 = im2.load()
            for x in range(0, width1):
                for y in range(0, height1):
                    if px1[x, y] != px2[x, y]:
                        log.debug("[TEST FAILED]: RGB:{0} is not the same RGB:{1}".format(px1[x, y], px2[x, y]))
                        return False
        return True


    def compare_image_by_histogram(self, res, des):
        image1 = Image.open(res)
        image2 = Image.open(des)
        h1 = image1.histogram()
        h2 = image2.histogram()
        rms = math.sqrt(reduce(operator.add,
                               map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
        return rms

