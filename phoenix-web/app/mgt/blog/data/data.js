/*
** Author: Fengchunyang
** Date: 2021/2/28 13:32
** Blog: http://www.fengchunyang.com
*/

import {urls} from "../../../../config/urls.js";
import {
    layTableReload, layTableToolBar, tableRowEventHandle, tableToolbarEventHandle, layerIframe,
    assigmentAttribute, tableBulkDelete
} from "../../../../common/utils.js";
import {params} from "../../../../config/params.js";

// 博客分类table表格
const initialArticleClassifyTable = ()=> {
    layui.table.render({
        elem: params.classifyTableElem,
        url: urls.classifyListApi,
        id: params.classifyTableID,
        page: true,
        limit: 15,
        limits: [15, 30, 45, 60, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter', layTableToolBar.add, layTableToolBar.delete],
        width: params.tableWidth,
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
        defaultToolbar: ['filter', layTableToolBar.add, layTableToolBar.delete],
        width: params.tableWidth,
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

// 博客分类新增/编辑事件
const classifyAddEvent = (obj, type='新增') => {
    layerIframe(urls.articleClassifyPage, `${type}博客分类`, 'classifyIframe', ['30rem', '17rem']);
};

// 博客分类批量删除事件
const classifyBulkDeleteEvent = (obj) => {
    tableBulkDelete(obj, urls.classifyListApi);
};

// 博客标签新增/编辑事件
const tagAddEvent = (obj, type='新增') => {
    layerIframe(urls.articleTagPage, `${type}博客标签`, 'tagIframe', ['30rem', '17rem']);
};

// 博客标签批量删除事件
const tagBulkDeleteEvent = (obj) => {
    tableBulkDelete(obj, urls.tagListApi);
};

// 博客分类编辑事件
const classifyEditEvent = (obj) => {
    assigmentAttribute(window, params.classifyFormFilter, obj.data);
    classifyAddEvent('编辑');
};

// 博客标签编辑事件
const tagEditEvent = (obj) => {
    assigmentAttribute(window, params.tagFormFilter, obj.data);
    tagAddEvent('编辑');
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
        tableToolbarEventHandle(obj, classifyAddEvent, classifyBulkDeleteEvent);
    });

    // 监听表格行工具事件
    layui.table.on(`tool(${params.classifyTableFilter})`, function (obj) {
        tableRowEventHandle(obj, urls.classifyInfoApi, null, classifyEditEvent);
    });

    // 监听表格头部工具事件
    layui.table.on(`toolbar(${params.tagTableFilter})`, function (obj) {
        tableToolbarEventHandle(obj, tagAddEvent, tagBulkDeleteEvent);
    });

    // 监听表格行工具事件
    layui.table.on(`tool(${params.tagTableFilter})`, function (obj) {
        tableRowEventHandle(obj, urls.tagInfoApi, null, tagEditEvent);
    });
});

