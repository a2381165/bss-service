# -*- coding: utf-8 -*-

from flask import Blueprint

version = "bossv3"

app = Blueprint('api', __name__)

# base
from controllers import AdminAuthorityApi
from controllers import UserLoginApi
from controllers import UserApi
from controllers import UserRoleApi
# from controllers import UserLogApi
from controllers import RoleApi
from controllers import RoleMenuApi
from controllers import OrganizationApi
from controllers import MenuApi
from controllers import AreaApi
from controllers import VersionApi
from controllers import UserRoleCheckApi

# spider

from controllers import SpiderNodeApi
from controllers import SpiderScriptApi
from controllers import SpiderDeployApi
from controllers import SpiderFailUrlApi
from controllers import SpiderProjectApi
from controllers import SpiderScheduleApi
from controllers import SpiderScriptNodeApi
from controllers import SpiderScriptScheduleApi
from controllers import TokenRefreshApi
from controllers import AdminLogApi

# data
from controllers import DataSourceApi
from controllers import CategoryApi
from controllers import CategoryInsertApi
from controllers import DataAreaApi
from controllers import DataAreaSetApi

from controllers import CrawlerApi
from controllers import TempItemApi
from controllers import DepartmentApi
from controllers import LabelApi
from controllers import DeptImgGet
from controllers import IndustryApi
from controllers import DeptItemApi
from controllers import ItemApi
from controllers import ItemContentAttachApi
from controllers import ItemContentApi

# appPreview
from controllers import appMinApi

# workbench
from controllers import WorkbenchApi
from controllers import WorkDataSourceApi

# dataCopy
# from common.demos import getOut

# uplaod
from controllers import uploadFileApi

# 咨詢師
from controllers import UserDeptAreaApi
from controllers import ItemServerApi
from controllers import TempServiceApi
# from controllers import AidanceApi
from controllers import NewAidanceApi
# from controllers import TaskAidanceApi
from controllers import ServiceAttachApi

# 咨询师 order
from controllers import UserOrderAssignApi
from controllers import UserOrderEditApi
from controllers import UserOrderAcceptApi
from controllers import UserOrderFileApi
from controllers import UserOrderProjectApi
from controllers import UserOrderContractApi
from controllers import UserOrderApi
from controllers import OrderAidanceTApi

# 流程
from controllers import WorkFlowApi
from controllers import SubFlowApi

# 通用
from controllers import CommonApi
from controllers import currencyApi
# 沟通
from controllers import CommunicateApi
from controllers import ProductServiceApi
from controllers import PotentialCustomersApi
from controllers import MemberEnterpriseCertificationApi
from controllers import MemberEnterpriseCertificationCheckApi
from controllers import ServiceApi

# 不通用流程 接口
from controllers import flowApi

# 银行
from controllers import BankPartnerApi
from controllers import BankProductApi

# 合同
from controllers import tempContractFlowApi
from controllers import MemberContractApi

# 渠道
from controllers import  UserTaskApi

# 项目结算
from controllers import  ContractSettlementApi

# 商务协助
from controllers import FlowSingleServiceApi
from controllers import FlowWholeServiceApi

from controllers import UserInternalOrderApi

# 项目 结算
from controllers import EditCostApi
from controllers import ServiceFeeApi
