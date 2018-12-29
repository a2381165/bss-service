# coding:utf-8
from config import runmodel, craeteapi

if __name__ == '__main__':
    headType = ["boss_","zzh_","data_","channel_"]
    # runmodel.main(["data_item","data_industry","data_label","data_item_industry","data_item_label","data_album","data_item_content","data_item_contentAttach"])
    # runmodel.main(['zzh_user_order', 'zzh_user_order_accept', 'zzh_user_order_amount', 'zzh_user_order_amount_check',
    #                'zzh_user_order_amount_failed', 'zzh_user_order_assess', 'zzh_user_order_assign',
    #                'zzh_user_order_audit', 'zzh_user_order_cancel', 'zzh_user_order_comment',
    #                'zzh_user_order_contract', 'zzh_user_order_coupon', 'zzh_user_order_edit', 'zzh_user_order_file',
    #                'zzh_user_order_invited', 'zzh_user_order_invoice', 'zzh_user_order_item',
    #                'zzh_user_order_project', 'zzh_user_order_refund_amount', 'zzh_user_order_service'])
    # runmodel.main(["boss_monthly_wages","boss_edit_cost","boss_service_fee"],dataType=headType[0])
    # runmodel.main(["zzh_user_internal_order"],dataType=headType[0])
    # craeteapi.main(["zzh_member_enterprise_contact_info","zzh_member_enterprise_contact_info_check"],dataType=headType[1])
    craeteapi.main(["zzh_user_internal_order"],dataType=headType[1],dataModel=2,flowId="ddff")
    # craeteapi.main(["boss_service_fee"],dataType=headType[0],dataModel=1)
    # runmodel.main(["boss_order_aidance_check"],dataType=headType[0])
    # runmodel.main(["data_work_flow","data_sub_flow","data_aidance"])
    # lists =runmodel.list_table()
    # for _ in lists:
    #     print (_)
    # craeteapi.main(["boss_communicate"],headType[0])
    # craeteapi.main(['zzh_user_order', 'zzh_user_order_accept', 'zzh_user_order_amount', 'zzh_user_order_amount_check',
    #                'zzh_user_order_amount_failed', 'zzh_user_order_assess', 'zzh_user_order_assign',
    #                'zzh_user_order_audit', 'zzh_user_order_cancel', 'zzh_user_order_comment',
    #                'zzh_user_order_contract', 'zzh_user_order_coupon', 'zzh_user_order_edit', 'zzh_user_order_file',
    #                'zzh_user_order_invited', 'zzh_user_order_invoice', 'zzh_user_order_item',
    #                'zzh_user_order_project', 'zzh_user_order_refund_amount', 'zzh_user_order_service'])
"view_aidance_check_flow_data_single_service"
"--registry-mirror=http://d7e77b19.m.daocloud.io"
