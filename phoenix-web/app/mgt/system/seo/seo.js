/*
** Author: Fengchunyang
** Date: 2021/3/4 15:38
** Blog: http://www.fengchunyang.com
*/
import {urls} from "../../../../config/urls.js";
import {params} from "../../../../config/params.js";
import {asyncApiResolve, layTableToolBar, tableToolbarEventHandle} from "../../../../common/utils.js";


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
        defaultToolbar: ['filter', layTableToolBar.add],
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

const pushApi = (obj) => {
    let selectData = layui.table.checkStatus(params.urlTableID);

    if (selectData.data.length === 0) {
        layui.layer.msg('请选择推送链接！')
    } else {
        let pushData = selectData.data.map(obj => {
            return obj.link
        })
        layui.layer.confirm(`是否推送以下数据:<br>${pushData.join("<br>")}`, {
            icon: 3,
            title: '确认提示'
        }, function (index) {
            asyncApiResolve(urls.articlePushApi, {"data": pushData.join("\n")}, 'post', (res) => {
                layui.layer.alert(`推送成功：${res.data.success} 条<br>剩余推送：${res.data.remain} 条<br>
                                   不是本站：${res.data.not_same_site || "无"}<br>不合法：${res.data.not_valid || "无"}`)
            })
            layui.layer.close(index)
        })
    }
}

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 初始化表格
    initialUrlListTable();

    // 监听表格头部工具事件
    layui.table.on('toolbar(urlListTableFilter)', function (obj) {
        pushApi(obj);
    });
});

