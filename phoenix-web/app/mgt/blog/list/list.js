/*
** Author: Fengchunyang
** Date: 2021/2/26 11:21
** Blog: http://www.fengchunyang.com
*/
import {urls} from "../../../../config/urls.js";
import {
    generateLaySwitch, layTableReload, asyncApiResolve, getLaySelectItem, syncApiResolve, tableRowEventHandle,
    getCurrentDate,
} from "../../../../common/utils.js";
import {params} from "../../../../config/params.js";

// 替换table中is_publish字段的显示样式
const isPublishResolve = (data) => {
    return generateLaySwitch(params.isPublish, '是|否', data.is_publish, params.isPublish, params.isPublish, data.id)
};

// 替换table中is_top字段的显示样式
const isTopResolve = (data) => {
    return generateLaySwitch(params.isTop, '是|否', data.is_top, params.isTop, params.isTop, data.id)
};

// 替换table中的tags字段
const tagsResolve = (data) => {
    const tagName = data.tags.map(item=>item.name);
    return tagName.join(',')
};

// 博客文章table表格
const initialArticleListTable = ()=> {
    layui.table.render({
        elem: params.articleTableElem,
        url: urls.articleListApi,
        id: params.articleTableID,
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
            {field: 'id', title: 'ID', align: "center", sort: true, hide: true},
            {field: 'classify', title: '分类', align: "center"},
            {field: 'tags', title: '标签', align: "center", templet: (d) => {return tagsResolve(d)}},
            {field: 'title', title: '标题', align: "center"},
            {field: 'desc', title: '简介', align: "center"},
            {field: 'content', title: '正文', align: "center"},
            {field: 'creator', title: '作者', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center"},
            {field: 'mtime', title: '修改时间', align: "center"},
            {field: 'etime', title: '编辑时间', align: "center"},
            {field: 'is_publish', title: '发布', align: "center", templet: (d) => {return isPublishResolve(d)}},
            {field: 'is_top', title: '置顶', align: "center", templet: (d) => {return isTopResolve(d)}},
            {fixed: 'right', title: '操作', align: 'center', toolbar: '#actionBar'}
        ]]
    })
};

// 监听表格发表/置顶switch切换事件
const monitorTableEvent = (filter, data) => {
    layer.confirm('确定?', {icon: 1, title: '操作确认'}, function (index) {
        let json_data = {};
        json_data[filter] = data.elem.checked ? 1 : 0;  // 如果当前为关闭状态则赋值0，否则赋值1

        // 如果是发布按钮，则仅当发布状态为true时，修改发布时间
        if (filter === params.isPublish && data.elem.checked) {
            json_data['ptime'] = getCurrentDate('-', '-', '');
        }

        const url = `${urls.articleInfoApi}/${data.elem.getAttribute('pk')}`;
        const response = syncApiResolve(url, json_data, 'patch');

        if (response.result === params.resSuccessTip) {
            // 关闭当前提示框
            layTableReload(params.articleTableID);
            parent.layui.layer.close(index);
        }
    }, function () {
        data.elem.checked = !data.elem.checked;  // 取消操作后，重置switch状态
        layui.form.render();
    });
};

// 页面加载后的动态操作
layui.jquery(document).ready(function () {
    // 渲染文章列表表格
    initialArticleListTable();

    // 动态加载博客分类数据
    getLaySelectItem(urls.classifyListApi, params.classifySelectElem, 'id', 'name');

    // 动态加载博客标签数据
    getLaySelectItem(urls.tagListApi, params.tagSelectElem, 'id', 'name');

    // 监听表格事件
    layui.table.on(`tool(${params.articleTableFilter})`, function (obj) {
        switch (obj.event) {
            case params.isPublish:
                layui.layer.msg('is publish');
                break;
            case params.isTop:
                layui.layer.msg('is top');
                break;
        }
    });

    // 监听table表格switch切换事件
    layui.form.on(`switch(${params.isPublish})`, function (data) {
        monitorTableEvent(params.isPublish, data);
    });

    // 监听table表格switch切换事件
    layui.form.on(`switch(${params.isTop})`, function (data) {
        monitorTableEvent(params.isTop, data);
    });

    // 监听搜索表单提交事件
    layui.form.on(`submit(${params.articleSearchForm})`, function (data) {
        layTableReload(params.articleTableID, data.field);
        return false
    });

    // 监听表格行工具事件
    layui.table.on(`tool(${params.articleTableFilter})`, function (obj) {
        const articleEditEvent = (obj) => {
            // 将被编辑的文章ID传入到博客文章页面，进行表单的初始赋值
            window.location.href = `${urls.articleInfoPage}?articleID=${obj.data.id}`
        };

        tableRowEventHandle(obj, urls.articleInfoApi, null, articleEditEvent);
    });
});

