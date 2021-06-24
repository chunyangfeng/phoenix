import {params} from "../../../../config/params.js";
import {urls} from "../../../../config/urls.js";
import {layTableReload} from "../../../../common/utils.js";

const initialAccessRecordTable = () => {
    layui.table.render({
        elem: '#access-record-list-table',
        url: urls.accessRecordListApi,
        id: 'access-record-list-table',
        page: true,
        limit: 15,
        limits: [15, 30, 45, 60, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter',],
        width: params.tableWidth,
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'atime', title: '访问时间', align: "center", width: 200},
            {field: 'path', title: '目标地址', align: "center"},
            {field: 'user_agent', title: 'UserAgent', align: "center"},
            {field: 'address', title: 'IP地址', align: "center", width: 180},
            {field: 'source', title: '地址来源', align: "center"},
            {field: 'spider', title: '蜘蛛类型', align: "center"},
            // {field: 'query_str', title: '查询字符串', align: "center"},
            {field: 'referer', title: '关联页面', align: "center"},
        ]]
    })
}

const initialAccessTimePicker = () => {
    layui.laydate.render({
        elem: '#accessTime',
        trigger: 'click',
    })
}

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 初始化表格
    initialAccessRecordTable();

    // 初始化日期控件
    initialAccessTimePicker();

    // 监听搜索表单提交事件
    layui.form.on('submit(accessRecordSearchForm)', function (data) {
        layTableReload('access-record-list-table', data.field);
        return false
    });
});