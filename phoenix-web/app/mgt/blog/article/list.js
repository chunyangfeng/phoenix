/*
** Author: Fengchunyang
** Date: 2021/2/26 11:21
** Blog: http://www.fengchunyang.com
*/
import {urls} from "../../../../config/urls.js";
import {generateLaySwitch} from "../../../../common/utils.js";
import {apiConfig} from "../../../../common/api.js";
import {api} from "../../../../common/api.js";
import {permissions} from "../../../../config/permission.js";

// 局部变量设置
const params = {
    isPublish: 'isPublish',
    isTop: 'isTop',
    tableElem: '#article-list-table',
    tableID: 'articleListTable',
    tableFilter: 'articleListTableFilter',
};

// 替换table中is_publish字段的显示样式
const isPublishResolve = (data) => {
    return generateLaySwitch(params.isPublish, '是|否', data.is_publish, params.isPublish, params.isPublish, data.id)
};

// 替换table中is_top字段的显示样式
const isTopResolve = (data) => {
    return generateLaySwitch(params.isTop, '是|否', data.is_top, params.isTop, params.isTop, data.id)
};

// 博客文章table表格
const initialArticleListTable = ()=> {
    layui.table.render({
        elem: params.tableElem,
        url: urls.articleListApi,
        id: params.tableID,
        page: true,
        limit: 10,
        limits: [10, 20, 40, 80, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter',],
        width: layui.jquery(window).width() - 290,  // 获取屏幕宽度，减去左侧导航条的宽度
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'id', title: 'ID', align: "center", sort: true, hide: true},
            {field: 'classify', title: '分类', align: "center"},
            {field: 'title', title: '标题', align: "center"},
            {field: 'desc', title: '简介', align: "center"},
            {field: 'content', title: '正文', align: "center"},
            {field: 'creator', title: '作者', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center"},
            {field: 'mtime', title: '修改时间', align: "center"},
            {field: 'etime', title: '编辑时间', align: "center"},
            {field: 'is_publish', title: '发布', align: "center", templet: function (d) {return isPublishResolve(d)}},
            {field: 'is_top', title: '置顶', align: "center", templet: function (d) {return isTopResolve(d)}},
            {fixed: 'right', title: '操作', align: 'center', toolbar: '#actionBar'}
        ]]
    })
};

// 监听表格事件
const monitorTableEvent = () => {

};

// 页面加载后的动态操作
layui.jquery(document).ready(function () {
    initialArticleListTable();

    // 监听表格事件
    layui.table.on(`tool(${params.tableFilter})`, function (obj) {
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
        let config = Object.assign({}, apiConfig);
        config.url = `${urls.articleInfoApi}/${data.elem.getAttribute('pk')}`;
        config.method = 'patch';
        config.data = {
            is_publish: data.value
        };
        api(config, permissions.ARTICLE);
    });
});

