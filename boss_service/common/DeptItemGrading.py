# coding:utf-8
class Node:
    def __init__(self, id, name, code, pcode, deptId, type,remark,children):
        self.id = id
        self.text = name
        self.code = code
        self.pcode = pcode
        self.deptId = deptId
        self.type = type
        self.remark = remark
        self.children = children

    def __delattr__(self, item):
        pass

    def get(self):
        if self.children:
            dicts = dict(id=self.id, text=self.text, code=self.code, pcode=self.pcode, deptId=self.deptId,type=self.type,remark=self.remark,
                         children=[])
            for nextNode in self.children:
                dicts["children"].append(nextNode.get())
        else:
            dicts = dict(id=self.id, text=self.text, code=self.code, pcode=self.pcode, deptId=self.deptId, type=self.type,remark=self.remark,)
        return dicts


def getDeptItem(infoList, code="000000"):
    try:
        resultList = []
        for dept in infoList:
            if dept.pcode == code:
                node = Node(dept.id, dept.name, dept.code, dept.pcode, dept.dept_id,dept.type,dept.remark, [])
                resultList.append(node)
        for sub in resultList:
            menu2 = _query_sub_menu_info(sub.code,infoList)
            if len(menu2):
                sub.children = getDeptItem(infoList, sub.code)
            else:
                sub.__delattr__('children')
        # 子菜单列表不为空
        if len(resultList):
            return resultList
        else:  # 没有子菜单了
            return None
    except Exception as e:
        print e
        return []


def _query_sub_menu_info(code, infoList):
    resultList = []
    for dept in infoList:
        if dept.pcode == code:
            resultList.append(dept)
    return resultList