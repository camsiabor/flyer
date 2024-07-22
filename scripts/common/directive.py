import logging
import os
import xml.etree.ElementTree as ET

from scripts.common.fileutil import FileUtil
from scripts.common.serial import TypeList
from scripts.common.sim import Collection


# DNode ===================================================================================== #
class DNode:

    def __init__(
            self,
            element: ET.Element = None,
            src: str = "",
            des: str = "",
            converge: str = "",
            action: str = "",
            category: str = "",
    ):
        self.element = element
        self.src = src
        self.des = des
        self.action = action
        self.category = category
        self.converge = converge
        self.init(element)
        pass

    def init(self, element: ET.Element):
        self.element = element
        self.src = element.attrib.get('src', '')
        self.des = element.attrib.get('des', '')
        self.action = element.attrib.get('action', '')
        self.category = element.attrib.get('category', '')
        self.converge = element.attrib.get('converge', '')
        return self


# DValue ===================================================================================== #

class DValue:

    def __init__(
            self,
            element: ET.Element = None,
            parent: ET.Element = None,
            text: str = "",
            value: any = None,
            active: str = '1',
    ):
        self.element = element
        self.parent = parent
        self.text = text
        self.value = value
        self.convert = False
        self.active = active
        self.init()
        pass

    def init(self):
        if self.element is None:
            return self
        self.text = self.element.text.strip()
        self.active = self.element.attrib.get('active', '1')
        return self

    def __str__(self):
        return self.text


# DData ===================================================================================== #


class DData:
    def __init__(
            self,
            element: ET.Element = None,
            src: str = "",
            des: str = "",
            base: str = "",
            active: str = '1',
    ):
        self.element = element
        self.src = src
        self.des = des
        self.base = base
        self.active = active
        self.content = DValue(active=active, parent=element)
        self.items = TypeList(DValue)
        self.init(element)
        pass

    def __iter__(self):
        yield self.content
        yield from self.items

    def __str__(self):
        ret = ""
        for item in self:
            ret += (str(item) + ",")
        return ret

    def init(self, element: ET.Element):
        if element is None:
            return self
        self.src = element.attrib.get('src', '')
        self.des = element.attrib.get('des', '')
        self.base = element.attrib.get('base', '')
        self.active = element.attrib.get('active', '1')
        self.content.text = element.text.strip()
        for tag in ['i', 'item']:
            for data_element in element.findall(tag):
                dv = DValue(element=data_element)
                self.items.append(dv)

        return self

    def infer(self, src_def: str):

        if self.active == '0' or self.active == 'false':
            return 0

        src = self.src
        if not src:
            src = src_def

        if not src:
            raise ValueError('src is empty')

        count = 0

        is_text = src in ['text']
        is_eval = src in ['eval']
        is_file = src in ['file']

        for one in self:

            if one.active == '0' or one.active == 'false':
                continue

            if is_text:
                one.value = one.text
                one.convert = True
                count += 1
                continue

            if not one.text:
                continue

            if is_eval:
                one.value = eval(one.text)
                one.convert = True

            if is_file:
                file_name = one.text.strip()
                file_path = os.path.join(self.base + "/", file_name)
                one.value = Directorate.load_and_embed(file_path)
                one.convert = True

            if one.convert:
                count += 1

        return count


# Directive =============================================================================== #
class Directive:
    def __init__(
            self,
            text: str = "",
            root: DNode = None,
            prefix="<OvO",
            suffix="</OvO>",
            logger_name=__name__,
    ):
        self.text = text.strip()
        self.root = root
        self.data = TypeList(DData)
        self.prefix = prefix
        self.suffix = suffix
        self.logger = logging.getLogger(logger_name)
        if text:
            self.parse(self.text)
        pass

    def __iter__(self):
        for data in self.data:
            if data is None:
                continue
            for one in data:
                if one is None:
                    continue
                yield data, one
        pass

    def parse(self, text) -> str:
        if not text:
            msg = 'empty text'
            self.logger.error(msg)
            return msg
        if not text.startswith(self.prefix) or not text.endswith(self.suffix):
            msg = 'prefix & suffix unmatched:\n' + text
            self.logger.error(msg)
            return msg
        root = ET.fromstring(text)
        self.root = DNode(element=root)
        for tag in ['d', 'data']:
            for data_element in root.findall(tag):
                self.data.append(DData(element=data_element))
        return ''

    def infer(self) -> any:
        for data, _ in self:
            data.infer(self.root.src)
        return self.converge()

    def converge(self):
        ret = None
        if self.root.des in ['dict', 'object', '']:
            ret = {}
            for data, one in self:
                if not one.convert:
                    continue
                Collection.merge_dict(ret, one.value)

        if self.root.des in ['list', 'tuple', 'array']:
            ret = []
            is_sep = 'seperate' in self.root.converge
            for data, one in self:
                if not one.convert:
                    continue
                if not is_sep and isinstance(one.value, (list, tuple)):
                    Collection.merge_list(ret, one.value)
                else:
                    ret.append(one.value)
        return ret


# ================================================================================================== #

class Directorate:

    @staticmethod
    def load_and_embed(file_path) -> any:
        config = FileUtil.load(file_path)
        return Directorate.embed(config)

    @staticmethod
    def embed(
            data: (dict, list, tuple),
            prefix: str = '<OvO',
            suffix: str = '</OvO>',
    ) -> any:

        if data is None:
            return None

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    value_strip = value.strip()
                    if value_strip.startswith(prefix) and value_strip.endswith(suffix):
                        directive = Directive(text=value, prefix=prefix, suffix=suffix)
                        parsed = directive.infer()
                        data[key] = Directorate.embed(parsed)
                        continue

                Directorate.embed(value)
            return data

        if isinstance(data, (list, tuple)):
            for i, item in enumerate(data):
                if isinstance(item, str) and item.startswith(prefix) and item.endswith(suffix):
                    directive = Directive(text=item, prefix=prefix, suffix=suffix)
                    parsed = directive.infer()
                    data[i] = Directorate.embed(parsed)
                else:
                    Directorate.embed(item)
            return data

        return data
