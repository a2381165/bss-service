# coding:utf-8


class Node:
    def __init__(self, id, text, pcode, children, check=False):
        self.id = id
        self.text = text
        self.pcode = pcode
        self.children = children
        self.check = check

    def __delattr__(self, item):
        # del self[item]
        pass

    def get(self):
        if self.children:
            dicts = dict(areaCode=self.id, areaName=self.text, pcode=self.pcode, check=self.check,
                         children=[])
            for nextNode in self.children:
                dicts["children"].append(nextNode.get())
        else:
            dicts = dict(areaCode=self.id, areaName=self.text, menuIcoUrl=self.pcode, check=self.check, )
        return dicts


def set_menus(id, areaList, InfoList=[]):
    if InfoList == []:
        try:
            _subMenus = []
            for area in areaList:
                if area.p_code == id:
                    menuNode = Node(area.area_code, area.area_name, area.p_code, [])
                    _subMenus.append(menuNode)
            for sub in _subMenus:
                area2 = _query_sub_menu_info(sub.id, areaList)
                if len(area2):
                    sub.children = set_menus(sub.id, areaList)
                else:
                    sub.__delattr__('children')
            # 子菜单列表不为空
            if len(_subMenus):
                return _subMenus
            else:  # 没有子菜单了
                return None
        except Exception as e:
            print e
            return []
    else:
        try:
            _subMenus = []
            for area in areaList:
                first = False
                if area.p_code == id:
                    for result in InfoList:
                        if result.area_code == area.area_code:
                            first = True
                    if first:
                        menuNode = Node(area.area_code, area.area_name, area.p_code, [],True)
                    else:
                        menuNode = Node(area.area_code, area.area_name, area.p_code, [])
                    _subMenus.append(menuNode)
            for sub in _subMenus:
                area2 = _query_sub_menu_info(sub.id, areaList)
                if len(area2):
                    sub.children = set_menus(sub.id, areaList)
                else:
                    sub.__delattr__('children')
            # 子菜单列表不为空
            if len(_subMenus):
                return _subMenus
            else:  # 没有子菜单了
                return None
        except Exception as e:
            print e
            return []


def _query_sub_menu_info(id, menus):
    menuList = []
    for menu in menus:
        if menu.p_code == id:
            menuList.append(menu)
    return menuList
