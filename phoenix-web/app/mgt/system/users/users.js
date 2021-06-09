import {params} from "../../../../config/params.js";
import {urls} from "../../../../config/urls.js";
import {generateLaySwitch, layTableReload, syncApiResolve} from "../../../../common/utils.js";


// 替换table中字段的显示样式
const generateSwitch = (data, name) => {
    return generateLaySwitch(name, '是|否', data[name], name, name, data.id)
};

const initialUsersTable = () => {
    layui.table.render({
        elem: '#users-list-table',
        url: urls.userListApi,
        id: 'users-list-table',
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
            {field: 'username', title: '用户名', align: "center"},
            {field: 'real_name', title: '真名', align: "center"},
            {field: 'wechat', title: '微信', align: "center"},
            {field: 'email', title: '邮箱', align: "center"},
            {field: 'phone', title: '电话', align: "center"},
            {field: 'site', title: '关联站点', align: "center", hide: true},
            {field: 'allow_login', title: '允许登陆', align: "center",
                templet: (d) => {return generateSwitch(d, "allow_login")}},
            {field: 'is_builtin', title: '内置用户', align: "center", templet: (d) => {
                let result = d.is_builtin ? "内置" : "新建"
                return `<button class="layui-btn layui-btn-xs layui-btn-radius layui-btn-normal">${result}</button>`
            }},
            {field: 'ctime', title: '创建时间', align: "center"},
            // {fixed: 'right', title: '操作', align: 'center', width: 130, toolbar: '#actionBar'}
        ]]
    })
}

// 监听表格switch切换事件
const tableSwitchEvent = (filter, data) => {
    layer.confirm('确定?', {icon: 1, title: '操作确认'}, function (index) {
        let json_data = {};
        json_data[filter] = data.elem.checked ? 1 : 0;  // 如果当前为关闭状态则赋值0，否则赋值1

        const url = `${urls.userInfoApi}/${data.elem.getAttribute('pk')}`;
        const response = syncApiResolve(url, json_data, 'patch');

        if (response.result === params.resSuccessTip) {
            // 关闭当前提示框
            layTableReload("usersListTable");
            parent.layui.layer.close(index);
        }
    }, function () {
        data.elem.checked = !data.elem.checked;  // 取消操作后，重置switch状态
        layui.form.render();
    });
};

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 初始化表格
    initialUsersTable();

    // 监听table表格switch切换事件
    layui.form.on('switch(allow_login)', function (data) {
        tableSwitchEvent("allow_login", data);
    });

    // 监听搜索表单提交事件
    layui.form.on('submit(usersSearchForm)', function (data) {
        layTableReload('users-list-table', data.field);
        return false
    });
});