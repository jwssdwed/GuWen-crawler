from parsel import Selector
import requests
import re
from sqlalchemy.exc import IntegrityError
from typing import List
from utils import scopedsession

from db import CiAuthor

class Crawler(object):
    def __init__(self):
        pass

    def poetry_request(self, seek_type, pageno, value=''):
        url = 'http://qsc.zww.cn/getdata.asp'
        payload = {
            'seektype': seek_type,
            'seekvalue': value,
            'pageno': pageno
        }
        resp = requests.post(
            url,
            data=payload
        )
        return resp
    
    def get_authors_list(self, seek_type=1):
        """
        Get all authors from http://qsc.zww.cn/. The seek_type is always 1.
        """
        for i in range(1, 5):   # To-do: this is hardcode list page, currently, there are only 90 pages, but there should be another more intelligent way to get the total page Nos.
            req = self.poetry_request(1, i)
            content = req.content.decode('gb2312', 'ignore')    # Decode in Mandarin
            selector = Selector(text = content)
            content_in_script = selector.css('script').get()
            for line in content_in_script.splitlines():
                # Iterate each author list page
                if not line.startswith('parent.QTS.filllist'):
                    # This is html text line doesn't contain values we evaluate.
                    continue
                inner_selector = Selector(text = line)
                anchor_lines = inner_selector.css('a').getall()
                for anchor in anchor_lines:
                    # Interate each anchor tag
                    if re.match(r'.*doseek2\((10,.*,.*)\);.*', anchor): # doseek2(10, .*, .*) stands for a author possessing one/some poetry in this website.
                        author = re.search(r'(?<=\);">)[^\…]+', anchor).group(0)
                        seek_type, value, pageno = re.search(r'(?<=onclick="doseek2\()[^\)]+', anchor).group(0).split(',')
                        desc = self.get_author_info(seek_type, 1, value)   # Pageno should always be 1
                        with scopedsession() as session:
                            # Add every author to DB because adding a batch of keys may have some primary keys exist in the table, 
                            # and it will trigger rollback w/o adding the non-existing new keys.
                            session.add(
                                CiAuthor(
                                    name = author,
                                    desc = desc
                                )
                            )


    def get_author_info(self, seek_type, pageno, value) -> str:
        """
        Author info are in doseek2(10, x, y), and a author's corresponding doseek2 func value could be retrived
        from the given author list page.

        Example::
        <a href="#" onclick="doseek2(10,1,1);">苏轼</a>
        """
        req = self.poetry_request(seek_type, pageno, value)
        content = req.content.decode('gb2312', 'ignore')
        for line in content.splitlines():
            if line.startswith('parent.QTS.fillbody'):
                # Process the description.
                desc = re.search(r'(?<=&nbsp;&nbsp;&nbsp;&nbsp;).*主要作品有', line) 
                # Some author doesnt have 主要作品有 in description.
                desc = desc.group(0)[0:-5] if desc else re.search(r'(?<=&nbsp;&nbsp;&nbsp;&nbsp;).*', line).group(0)

                desc = desc.replace('             ', '')    # Remove the unnecessary spaces/tabs
                desc = re.sub('[\<br\>|\<\/br\>|\<front\>|\<\/front>|\<b\>|\<\/b\>]', '', desc) # Remove extral tags.
                return desc

    def get_ci_list(self, seek_type=2, pageno=1, value=""):
        """

        """
        for i in range(pageno + 1):
            pass

crawler_worker = Crawler()
crawler_worker.get_authors_list()
