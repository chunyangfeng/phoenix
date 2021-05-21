import {params} from "../../../../config/params.js";
import {urls} from "../../../../config/urls.js";


// 初始化数据表格
const initialTable = ()=> {
    layui.table.render({
        elem: "#friendly-link-list-table",
        url: urls.flinkListApi,
        id: "friendly-link-list-table",
        page: true,
        limit: 10,
        limits: [10, 20, 40, 80, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter', ],
        width: params.tableWidth,
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'name', title: '网站名称', align: "center"},
            {field: 'site', title: '网站地址', align: "center"},
            {field: 'logo', title: '网站Logo', align: "center"},
            {field: 'enable', title: '是否启用', align: "center"},
            {field: 'link', title: '校验地址', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center", width: 200},
        ]]
    })
};

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 初始化表格
    initialTable();
});