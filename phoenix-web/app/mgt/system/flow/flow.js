/*
** Author: Fengchunyang
** Date: 2021/3/5 10:20
** Blog: http://www.fengchunyang.com
*/
import {params} from "../../../../config/params.js";
import {urls} from "../../../../config/urls.js";
import {
    layerIframe, tableBulkDelete, tableToolbarEventHandle, layTableToolBar, assigmentAttribute, tableRowEventHandle,
    syncApiResolve, layTableReload, getCurrentDate
} from "../../../../common/utils.js";


// 项目信息table表格
const initialProjectInfoTable = ()=> {
    layui.table.render({
        elem: params.projectInfoTableElem,
        url: urls.projectInfoListApi,
        id: params.projectInfoTableID,
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
            {field: 'name', title: '项目名称', align: "center"},
            {field: 'stime', title: '开始时间', align: "center"},
            {field: 'etime', title: '结束时间', align: "center"},
            {field: 'dtime', title: '完成时间', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center"},
            {field: 'mtime', title: '修改时间', align: "center"},
            {field: 'status_display', title: '状态', align: "center"},
            {fixed: 'right', title: '操作', align: 'center', toolbar: '#actionBar'}
        ]]
    })
};

// 替换table中的status字段
const statusResolve = (data) => {
    const pubClassAttr = "layui-btn layui-btn-radius layui-btn-xs"
    const statusMap = {
        "已完成": `${pubClassAttr}`,
        "计划中": `${pubClassAttr} layui-btn-warm`
    }
    return `<button type="button" class="${statusMap[data.status_display]}">${data.status_display}</button>`
};

// 替换table中的priority字段
const priorityResolve = (data) => {
    const pubClassAttr = "layui-btn layui-btn-radius layui-btn-xs"
    const statusMap = {
        "一般": `${pubClassAttr} layui-btn-normal`,
        "重要": `${pubClassAttr} layui-btn-warm`,
        "紧急": `${pubClassAttr} layui-btn-danger`
    }
    return `<button type="button" class="${statusMap[data.priority_display]}">${data.priority_display}</button>`
};


// 项目任务table表格
const initialProjectTaskTable = ()=> {
    layui.table.render({
        elem: params.projectTaskTableElem,
        url: urls.projectTaskListApi,
        id: params.projectTaskTableID,
        page: true,
        limit: 15,
        limits: [15, 30, 45, 60, 100],
        text: {
            none: "暂无相关数据",
        },
        toolbar: true,
        defaultToolbar: ['filter', layTableToolBar.add, layTableToolBar.delete, layTableToolBar.update],
        width: params.tableWidth,
        cellMinWidth: 100,
        cols: [[
            { fixed: 'left', title: '选中', align: "center", type: 'checkbox'},
            {field: 'id', title: 'ID', align: "center", sort: true, hide: true},
            {field: 'project_name', title: '所属项目', align: "center", width: 100},
            {field: 'priority_display', title: '优先级', align: "center", width: 100, templet: (d) => {return priorityResolve(d)}},
            {field: 'name', title: '任务名称', align: "center"},
            {field: 'remark', title: '备注说明', align: "center"},
            {field: 'ctime', title: '创建时间', align: "center", width: 180},
            // {field: 'dtime', title: '完成时间', align: "center"},
            // {field: 'record', title: '记录', align: "center"},
            {field: 'status_display', title: '状态', align: "center", width: 100, templet: (d) => {return statusResolve(d)}},
            {fixed: 'right', title: '操作', align: 'center', width: 130, toolbar: '#actionBar'}
        ]]
    })
};

// 项目信息新增/编辑事件
const projectInfoAddEvent = (obj, type='新增') => {
    layerIframe(urls.projectInfoAddPage, `${type}项目信息`, 'projectInfoIframe', ['40rem', '28rem']);
};

// 项目信息批量删除事件
const projectInfoBulkDeleteEvent = (obj) => {
    tableBulkDelete(obj, urls.projectInfoListApi);
};

// 项目任务新增/编辑事件
const projectTaskAddEvent = (obj, type='新增') => {
    layerIframe(urls.projectTaskAddPage, `${type}项目任务`, 'projectTaskIframe', ['40rem', '35rem']);
};

// 项目任务批量删除事件
const projectTaskDeleteEvent = (obj) => {
    tableBulkDelete(obj, urls.projectTaskListApi);
};

// 项目信息编辑事件
const projectInfoEditEvent = (obj) => {
    assigmentAttribute(window, params.projectInfoFormFilter, obj.data);
    projectInfoAddEvent('编辑');
};

// 项目任务编辑事件
const projectTaskEditEvent = (obj) => {
    assigmentAttribute(window, params.projectTaskFormFilter, obj.data);
    projectTaskAddEvent('编辑');
};

// 项目任务批量更新事件
const projectTaskUpdateEvent = (obj) => {
    let selectData = layui.table.checkStatus(params.projectTaskTableID);

    let instances_id = [];
    layui.jquery.each(selectData.data, (index, value) => {
        if (value.status !== 'done') {
            instances_id.push(value.id)
        }
    });

    if (instances_id.length === 0) {
        layui.layer.msg('请选择未完成的项目任务进行更新！');
        return
    }

    let putData = {
        status: 'done',
        instances_id: instances_id,
        dtime: getCurrentDate('-', '-', ''),
    };

    // 执行批量更新
    layui.layer.confirm('确定更新?', {icon: 1, title: '更新确认'}, function (index) {
        const response = syncApiResolve(urls.projectTaskListApi, putData, 'put');
        if (response.result === params.resSuccessTip) {
            parent.layui.table.reload(params.projectTaskTableID);  // 重载表格
            parent.layui.layer.close(index);
        }
    });
};


// 页面加载后的动态操作
layui.jquery(document).ready(() => {
    // 初始化项目信息表格
    initialProjectInfoTable();

    // 初始化项目任务表格
    initialProjectTaskTable();

    // 监听表格头部工具事件
    layui.table.on(`toolbar(${params.projectInfoTableFilter})`, function (obj) {
        tableToolbarEventHandle(obj, projectInfoAddEvent, projectInfoBulkDeleteEvent);
    });

    // 监听表格行工具事件
    layui.table.on(`tool(${params.projectInfoTableFilter})`, function (obj) {
        tableRowEventHandle(obj, urls.projectInfoInfoApi, null, projectInfoEditEvent);
    });

    // 监听表格头部工具事件
    layui.table.on(`toolbar(${params.projectTaskTableFilter})`, function (obj) {
        tableToolbarEventHandle(obj, projectTaskAddEvent, projectTaskDeleteEvent, projectTaskUpdateEvent);
    });

    // 监听表格行工具事件
    layui.table.on(`tool(${params.projectTaskTableFilter})`, function (obj) {
        tableRowEventHandle(obj, urls.projectTaskInfoApi, null, projectTaskEditEvent);
    });

    // 监听搜索表单提交事件
    layui.form.on(`submit(${params.projectTaskSearchForm})`, function (data) {
        layTableReload(params.projectTaskTableID, data.field);
        return false
    });
});
