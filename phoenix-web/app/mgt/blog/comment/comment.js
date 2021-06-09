import {params} from "../../../../config/params.js";
import {urls} from "../../../../config/urls.js";
import {
    generateLaySwitch, getCurrentDate,
    getLaySelectItem,
    layTableReload,
    syncApiResolve,
    tableRowEventHandle
} from "../../../../common/utils.js";


// 替换table中is_examine字段的显示样式
const isExamine = (data) => {
    return generateLaySwitch("is_examine", '是|否', data.is_examine, "is_examine", "is_examine", data.id)
};

// 替换table中is_reply字段的显示样式
const isReply = (data) => {
    return generateLaySwitch("is_reply", '是|否', data.is_reply, "is_reply", "is_reply", data.id)
};

// 留言table表格
const initialCommentListTable = ()=> {
    layui.table.render({
        elem: "#comment-list-table",
        url: urls.commentMgtListApi,
        id: "commentListTable",
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
            {fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'id', title: 'ID', align: "center", sort: true, hide: true},
            {field: 'article', title: '关联文章', align: "center"},
            {field: 'comment_content', title: '关联评论', align: "center"},
            {field: 'comment_id', title: '关联评论ID', align: "center", hide: true},
            {field: 'nickname', title: '留言者', align: "center"},
            {field: 'email', title: '邮箱', align: "center"},
            {field: 'content', title: '留言', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center"},
            {field: 'is_examine', title: '是否审核', align: "center", templet: (d) => {return isExamine(d)}},
            {field: 'is_reply', title: '是否回复', align: "center", templet: (d) => {return isReply(d)}},
            {fixed: 'right', title: '操作', align: 'center', toolbar: '#actionBar'}
        ]]
    })
};

const replyComment = (obj) => {
    layui.layer.prompt({
        formType: 2,
        title: '回复评论',
        area: ['500px', '250px']
    }, function(value, index, elem){
        let postData = {
            article_id: obj.data.article_id,
            comment: obj.data.id,
            nickname: "却邪水心",
            email: "admin@fengchunyang.com",
            content: value,
            is_examine: true,
            is_reply: true,
        };
        const response = syncApiResolve(urls.commentMgtListApi, postData, 'post');
        if (response.result === params.resSuccessTip) {
            layui.layer.msg("回复成功");
            // 回复成功后，将回复标记更新为已回复
            const url = `${urls.commentMgtInfoApi}/${obj.data.id}`;
            const response = syncApiResolve(url, {is_reply: 1}, 'patch');

            if (response.result === params.resSuccessTip) {
                layTableReload("commentListTable");
            }
            layui.layer.close(index);
        }
    });
}

// 监听表格switch切换事件
const tableSwitchEvent = (filter, data) => {
    layer.confirm('确定?', {icon: 1, title: '操作确认'}, function (index) {
        let json_data = {};
        json_data[filter] = data.elem.checked ? 1 : 0;  // 如果当前为关闭状态则赋值0，否则赋值1

        const url = `${urls.commentMgtInfoApi}/${data.elem.getAttribute('pk')}`;
        const response = syncApiResolve(url, json_data, 'patch');

        if (response.result === params.resSuccessTip) {
            // 关闭当前提示框
            layTableReload("commentListTable");
            parent.layui.layer.close(index);
        }
    }, function () {
        data.elem.checked = !data.elem.checked;  // 取消操作后，重置switch状态
        layui.form.render();
    });
};


// 页面加载后的动态操作
layui.jquery(document).ready(function () {
    // 渲染留言列表表格
    initialCommentListTable();

    // 监听搜索表单提交事件
    layui.form.on('submit(commentSearchForm)', function (data) {
        layTableReload("commentListTable", data.field);
        return false
    });

    // 监听table表格switch切换事件
    layui.form.on('switch(is_examine)', function (data) {
        tableSwitchEvent("is_examine", data);
    });

    // 监听table表格switch切换事件
    layui.form.on('switch(is_reply)', function (data) {
        tableSwitchEvent("is_reply", data);
    });

    // 监听表格行工具事件
    layui.table.on('tool(commentListTableFilter)', function (obj) {
        tableRowEventHandle(obj, urls.articleInfoApi, replyComment);
    });
});