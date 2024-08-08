import logging
import os
import random
import xml.etree.ElementTree as ET

from scripts.common.collection import Collection
from scripts.common.fileutil import FileUtil
from scripts.common.serial import TypeList


# DNode ===================================================================================== #
class DNode:

    def __init__(
            self,
            element: ET.Element = None,
            state: any = None,
            func_name: str = 'init',
            func_args: any = None,
            src: str = "",
            des: str = "",
            base: str = "",
            pick: str = "",
            action: str = "",
            converge: str = "",
            category: str = "",
            shell: int = 0,
    ):
        self.element = element
        self.state = state
        self.func_name = func_name
        self.func_args = func_args
        self.src = src
        self.des = des
        self.base = base
        self.pick = pick
        self.action = action
        self.category = category
        self.converge = converge
        self.shell = shell
        self.init(element)
        pass

    def init(self, element: ET.Element):
        self.element = element
        self.src = element.attrib.get('src', '').lower()
        self.des = element.attrib.get('des', '').lower()
        self.base = element.attrib.get('base', '')
        self.pick = element.attrib.get('pick', '').lower()
        self.action = element.attrib.get('action', '').lower()
        self.func_name = element.attrib.get('func', self.func_name)
        self.func_args = element.attrib.get('args', None)
        self.category = element.attrib.get('category', '').lower()
        self.converge = element.attrib.get('converge', '').lower()
        self.shell = int(element.attrib.get('shell', '0'))
        return self


# DValue ===================================================================================== #

class DValue:

    def __init__(
            self,
            element: ET.Element = None,
            state: any = None,
            func_name: str = 'init',
            func_arg: any = None,
            text: str = "",
            value: any = None,
            active: str = '1',
            parent: 'DData' = None,
    ):
        self.element = element
        self.state = state
        self.parent = parent
        self.func_name = func_name
        self.func_args = func_arg
        self.text = text
        self.value = value
        self.convert = False
        self.active = active
        self.parent = parent
        self.init()
        pass

    def init(self):
        if self.element is None:
            return self
        self.text = self.element.text.strip()
        self.active = self.element.attrib.get('a', '1').lower()
        self.func_name = self.element.attrib.get('func', self.func_name)
        self.func_args = self.element.attrib.get('args', None)
        return self

    def __str__(self):
        return self.text

    # DValue END
    pass


# DPick ===================================================================================== #

class DPick:

    def __init__(self, text: str):
        self.text = text
        self.init(self.text)
        pass

    def init(self, text: str):
        self.text = text.strip()
        return self

    pass



# DData ===================================================================================== #


class DData:
    def __init__(
            self,
            element: ET.Element = None,
            state: any = None,
            func_name: str = 'init',
            func_args: any = None,
            src: str = "",
            des: str = "",
            base: str = "",
            pick: str = "",
            active: str = '1',
            parent: 'DNode' = None,
    ):
        self.element = element
        self.state = state
        self.func_name = func_name
        self.func_args = func_args
        self.src = src
        self.des = des
        self.base = base
        self.pick = pick
        self.active = active
        self.content = DValue(active=active, parent=self, state=state)
        self.items = TypeList(DValue)
        self.parent = parent
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

    def __getitem__(self, index):
        size = len(self.items)
        if index == size:
            return self.content
        return self.items[index]

    def init(self, element: ET.Element):
        if element is None:
            return self
        self.src = element.attrib.get('src', self.parent.src).lower()
        self.des = element.attrib.get('des', self.parent.des).lower()
        self.pick = element.attrib.get('pick', self.parent.pick).lower()
        self.base = element.attrib.get('base', '')
        self.active = element.attrib.get('a', '1').lower()
        self.func_name = element.attrib.get('func', self.func_name)
        self.func_args = element.attrib.get('args', None)
        if not self.func_name:
            self.func_name = 'init'
        self.content.text = element.text.strip()
        if self.parent is not None:
            if self.src == 'file' and self.parent.base:
                self.base = os.path.join(self.parent.base + "/", self.base)

        for tag in ['i', 'item']:
            for data_element in element.findall(tag):
                dv = DValue(element=data_element, parent=self, state=self.state)
                if dv.active == '0' or dv.active == 'false':
                    self.element.remove(data_element)
                    continue
                self.items.append(dv)

        return self

    def infer_one(
            self,
            one: DValue,
            src: str,
    ) -> any:
        # print(f"[{count}] {one}")

        is_text = src in ['text']
        is_eval = src in ['eval']
        is_file = src in ['file']

        if one.active == '0' or one.active == 'false':
            return None

        if is_text:
            one.value = one.text
            one.convert = True
            return one.text

        text_strip = one.text.strip()

        if not text_strip:
            return None

        if is_eval:
            one.value = eval(text_strip)
            one.convert = True
            return one.value

        if is_file:
            self.infer_file(one, text_strip)
            return one.value

        raise ValueError(f"unsupported infer src: {src}")

    def infer(self, src_def: str) -> list:

        if self.active == '0' or self.active == 'false':
            return []

        src = self.src
        if not src:
            src = src_def

        if not src:
            raise ValueError('src is empty')

        ret = []

        if self.pick == 'rand':
            size = len(self.items)
            if size == 0:
                return ret
            if size == 1:
                one = self.items[0]
            else:
                index = random.randint(0, size)
                # not a bug, index == one -> fetch content, see DData.__getitem__()
                one = self[index]

            self.infer_one(one, src)
            ret.append(one.value)
            return ret

        for one in self:
            self.infer_one(one, src)
            if one.convert:
                ret.append(one.value)

        return ret

    def infer_file(self, one: DValue, text_strip: str):
        file_name = text_strip
        file_path = os.path.join(self.base + "/", file_name)
        func_name = one.func_name
        if not func_name:
            func_name = self.func_name
        func_args = one.func_args
        if not func_args:
            func_args = self.func_args
        one.value = Directorate.load_and_embed(
            file_path=file_path,
            func_name=func_name, func_args=func_args,
            state=self.state
        )
        one.convert = True
        return one.value


# Directive =============================================================================== #
class Directive:
    def __init__(
            self,
            text: str = "",
            root: DNode = None,
            prefix="<OvO",
            suffix="</OvO>",
            state: any = None,
            func_name: str = 'init',
            func_args: any = None,
            logger_name=__name__,
    ):
        self.text = text.strip()
        self.root = root
        self.data = TypeList(DData)
        self.prefix = prefix
        self.suffix = suffix
        self.state = state
        self.func_name = func_name
        self.func_args = func_args
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

    def __getitem__(self, index):
        return self.data[index]

    def parse(self, text) -> str:
        if not text:
            msg = 'empty text'
            self.logger.error(msg)
            return msg
        if not text.startswith(self.prefix) or not text.endswith(self.suffix):
            msg = 'prefix & suffix unmatched:\n' + text
            self.logger.error(msg)
            return msg
        try:
            root = ET.fromstring(text)
        except Exception as ex:
            self.logger.error(f"error: {ex} | text:\n {text}")
            raise ex

        self.root = DNode(
            element=root,
            state=self.state,
            func_name=self.func_name, func_args=self.func_args,
        )
        for tag in ['d', 'data']:
            for data_element in root.findall(tag):
                ddata = DData(
                    element=data_element, state=self.state,
                    parent=self.root,
                    func_name=self.root.func_name, func_args=self.root.func_args,
                )
                if ddata.active == '0' or ddata.active == 'false':
                    self.root.element.remove(data_element)
                    continue
                self.data.append(ddata)
        return ''

    def infer(self, converging: bool = True):

        if self.root.shell > 0:
            self.root.shell -= 1
            self.root.element.set('shell', str(self.root.shell))
            ret = ET.tostring(
                element=self.root.element,
                encoding='utf-8',
                method='xml'
            ).decode('utf-8')
            return ret

        if self.root.pick == 'rand':
            size = len(self.data)
            if size == 0:
                return None
            if size == 1:
                one = self.data[0]
            else:
                index = random.randint(0, size - 1)
                one = self.data[index]
            one.infer(self.root.src)
        else:
            for data in self.data:
                data.infer(self.root.src)

        if converging:
            return self.converge()

        return None

    def converge(self):
        ret = None

        is_text = self.root.des in ['str', 'string', 'text', '']
        is_dict = self.root.des in ['dict', 'object']
        is_list = self.root.des in ['list', 'tuple', 'array']
        is_sep = 'seperate' in self.root.converge

        if is_text:
            ret = ""
        elif is_dict:
            ret = {}
        elif is_list:
            ret = []

        for data, one in self:
            if not one.convert:
                continue

            if is_text:
                if isinstance(one.value, str):
                    ret += one.value
                elif isinstance(one.value, (list, tuple)):
                    ret += ''.join(one.value)
                else:
                    ret += str(one.value)
                continue

            if is_dict:
                Collection.dict_merge(ret, one.value)
                continue

            if is_list:
                if not is_sep and isinstance(one.value, (list, tuple)):
                    Collection.list_merge(ret, one.value)
                else:
                    ret.append(one.value)
                continue

        return ret


# ================================================================================================== #

class Directorate:

    @staticmethod
    def load_and_embed(
            file_path: str,
            func_name: str = 'init',
            func_args: any = None,
            state: any = None
    ) -> any:
        config = FileUtil.load(
            file_path=file_path,
            func_name=func_name,
            func_args=func_args,
            state=state,
        )
        return Directorate.embed(config)

    @staticmethod
    def embed(
            data: (dict, list, tuple),
            prefix: str = '<OvO',
            suffix: str = '</OvO>',
            func_name: str = 'init',
            func_args: any = None,
            state: any = None,
    ) -> any:

        if data is None:
            return None

        if isinstance(data, str):
            data_strip = data.strip()
            if data_strip.startswith(prefix) and data_strip.endswith(suffix):
                directive = Directive(
                    text=data_strip,
                    prefix=prefix, suffix=suffix,
                    func_name=func_name, func_args=func_args,
                    state=state,
                )
                return directive.infer()
            else:
                return data

        if isinstance(data, dict):
            clone = {**data}
            for key, value in clone.items():
                clone[key] = Directorate.embed(
                    data=value,
                    prefix=prefix, suffix=suffix,
                    func_name=func_name, func_args=func_args,
                    state=state,
                )
            return clone

        if isinstance(data, (list, tuple)):
            clone = [*data]
            for i, item in enumerate(clone):
                clone[i] = Directorate.embed(
                    data=item,
                    prefix=prefix, suffix=suffix,
                    func_name=func_name, func_args=func_args,
                    state=state,
                )
            return clone

        return data
