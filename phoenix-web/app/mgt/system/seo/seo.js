/*
** Author: Fengchunyang
** Date: 2021/3/4 15:38
** Blog: http://www.fengchunyang.com
*/
import {urls} from "../../../../config/urls.js";
import {params} from "../../../../config/params.js";


// sitemap表格
const initialUrlListTable = ()=> {
    layui.table.render({
        elem: params.urlTableElem,
        url: urls.urlListApi,
        id: params.urlTableID,
        page: true,
        limit: 10,
        limits: [10, 20, 40, 80, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter',],
        width: params.tableWidth,
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'classify_name', title: '分类', align: "center", width: 120},
            {field: 'tags', title: '标签', align: "center", width: 250},
            {field: 'title', title: '标题', align: "center"},
            {field: 'link', title: '链接', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center", width: 200},
            {field: 'mtime', title: '更新时间', align: "center", width: 200},
        ]]
    })
};

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 初始化表格
    initialUrlListTable();
});

