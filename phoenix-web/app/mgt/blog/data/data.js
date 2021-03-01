/*
** Author: Fengchunyang
** Date: 2021/2/28 13:32
** Blog: http://www.fengchunyang.com
*/

import {urls} from "../../../../config/urls.js";
import {layTableReload, layTableToolBar, tableRowEventHandle, tableToolbarEventHandle} from "../../../../common/utils.js";
import {params} from "../../../../config/params.js";

// 博客分类table表格
const initialArticleClassifyTable = ()=> {
    layui.table.render({
        elem: params.classifyTableElem,
        url: urls.classifyListApi,
        id: params.classifyTableID,
        page: true,
        limit: 10,
        limits: [10, 20, 40, 80, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter', layTableToolBar.add],
        width: layui.jquery(window).width() - 290,  // 获取屏幕宽度，减去左侧导航条的宽度
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'id', title: 'ID', align: "center", sort: true, hide: true},
            {field: 'name', title: '分类名称', align: "center"},
            {field: 'desc', title: '描述', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center"},
            {field: 'mtime', title: '修改时间', align: "center"},
            {fixed: 'right', title: '操作', align: 'center', toolbar: `${params.rowActionElem}`}
        ]]
    })
};

// 博客标签table表格
const initialArticleTagTable = ()=> {
    layui.table.render({
        elem: params.tagTableElem,
        url: urls.tagListApi,
        id: params.tagTableID,
        page: true,
        limit: 10,
        limits: [10, 20, 40, 80, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter', layTableToolBar.add],
        width: layui.jquery(window).width() - 290,  // 获取屏幕宽度，减去左侧导航条的宽度
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'id', title: 'ID', align: "center", sort: true, hide: true},
            {field: 'name', title: '标签名称', align: "center"},
            {field: 'desc', title: '描述', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center"},
            {field: 'mtime', title: '修改时间', align: "center"},
            {fixed: 'right', title: '操作', align: 'center', toolbar: `${params.rowActionElem}`}
        ]]
    })
};

// 博客分类新增事件
const classifyAddEvent = () => {
    layui.layer.open({
        type: 2,
        title: '新增博客分类',
        id: 'classifyIframe',
        skin: 'layui-layer-lan',
        area: ['30rem', '17rem'],
        content: urls.articleClassifyPage,
        width: 1000,
    })
};

// 博客标签新增事件
const tagAddEvent = () => {
    layui.layer.open({
        type: 2,
        title: '新增博客标签',
        id: 'tagIframe',
        skin: 'layui-layer-lan',
        area: ['30rem', '17rem'],
        content: urls.articleTagPage,
        width: 1000,
    })
};

// 博客分类行删除事件
const classifyRowDeleteEvent = () => {

};

// 页面加载后的动态操作
layui.jquery(document).ready(function () {
    initialArticleClassifyTable();
    initialArticleTagTable();

    // 监听搜索表单提交事件
    layui.form.on(`submit(${params.tagSearchForm})`, function (data) {
        layTableReload(params.tagTableID, data.field);
        return false
    });

    // 监听搜索表单提交事件
    layui.form.on(`submit(${params.classifySearchForm})`, function (data) {
        layTableReload(params.classifyTableID, data.field);
        return false
    });

    // 监听表格头部工具事件
    layui.table.on(`toolbar(${params.classifyTableFilter})`, function (obj) {
        tableToolbarEventHandle(obj, classifyAddEvent);
    });

    // 监听表格行工具事件
    layui.table.on(`tool(${params.classifyTableFilter})`, function (obj) {
        tableRowEventHandle(obj);
    });

    // 监听表格头部工具事件
    layui.table.on(`toolbar(${params.tagTableFilter})`, function (obj) {
        tableToolbarEventHandle(obj, tagAddEvent);
    });

    // 监听表格行工具事件
    layui.table.on(`tool(${params.tagTableFilter})`, function (obj) {
        tableRowEventHandle(obj);
    });
});

