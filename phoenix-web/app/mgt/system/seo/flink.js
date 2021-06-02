import {params} from "../../../../config/params.js";
import {urls} from "../../../../config/urls.js";
import {asyncApiResolve, layTableReload, syncApiResolve} from "../../../../common/utils.js";


// 初始化数据表格
const initialTable = ()=> {
    layui.table.render({
        elem: "#friendly-link-list-table",
        url: urls.flinkListApi,
        id: "friendly-link-list-table",
        page: true,
        limit: 15,
        limits: [15, 30, 45, 60, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter', ],
        width: params.tableWidth,
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'id', title: 'ID', align: "center", hide: true},
            {field: 'name', title: '网站名称', align: "center"},
            {field: 'site', title: '网站地址', align: "center"},
            {field: 'logo', title: '网站Logo', align: "center"},
            {field: 'enable', title: '是否启用', align: "center", templet: (obj)=> {
                if (obj.enable) {
                    return `<input lay-filter="isEnable" value="${obj.id}" type="checkbox" name="enable" lay-skin="switch" lay-text="启用|禁用" checked>`
                } else {
                    return `<input lay-filter="isEnable" value="${obj.id}" type="checkbox" name="enable" lay-skin="switch" lay-text="启用|禁用">`
                }
                }},
            {field: 'link', title: '校验地址', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center", width: 200},
        ]]
    })
};

const isEnable = (data) => {
    let putData = {
        enable: data.elem.checked?1:0,
        instances_id: [data.value,]
    }
    const response = syncApiResolve(urls.flinkListApi, putData, 'put');
    layui.table.reload('friendly-link-list-table');  // 重载表格
    layui.layer.msg("更新成功")
}

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 初始化表格
    initialTable();

    // 友链启停事件
    layui.form.on('switch(isEnable)', function (data) {
        isEnable(data)
    })
});