/*
** Author: Fengchunyang
** Date: 2021/2/23 10:45
** Blog: http://www.fengchunyang.com
*/

// 全局变量
import {params} from "../config/params.js";
import {api, apiConfig} from "./api.js";

export const $ = layui.jquery;

// 阻止表单自动提交
export const blockFormSubmit = () => {
    $("form").submit(function (event) {
        event.preventDefault();
    })
};

// 获取当前访问的url地址的相对路径
export const getRelativePath = ()=> {
    let url = document.location.toString();
    let arrUrl = url.split("//");

    let start = arrUrl[1].indexOf("/");
    let relUrl = arrUrl[1].substring(start);// stop省略，截取从start开始到结尾的所有字符

    if (relUrl.indexOf("?") !== -1) {
        relUrl = relUrl.split("?")[0];
    }
    return relUrl;
};

// 获取动态时钟
export const dynamicClock = (elem_id) => {
    let time = new Date();  //获得当前时间
    let year = time.getFullYear();  //获得年月日
    let month = time.getMonth();  //获得年月日
    let date = time.getDate();  //获得年月日
    let hour = time.getHours();  //获得小时、分钟、秒
    let minute = time.getMinutes();
    let second = time.getSeconds();

    // 分钟补0显示
    if (minute < 10) {
        minute = "0" + minute;
    }

    // 秒钟补0显示
    if (second < 10) {
        second = "0" + second;
    }

    // 设置文本框的内容为当前时间
    const datetime_str = year + "年" + month + "月" + date + "日 " + hour + ":" + minute + ":" + second;
    $('#'+elem_id).empty().append(datetime_str);
};

// 生成lay-switch
export const generateLaySwitch = (name, text, value, event, filter, pk) => {
    // 判断传入的value是否为true，如果为true，则默认开关为'开'，否则为'关'
    let is_check = '';
    if (value) {
        is_check = 'checked';
    }

    return `<input type='checkbox' name=${name} lay-skin='switch' lay-text=${text} value=${value} ` +
        `lay-event=${event} lay-filter=${filter} ${is_check} pk=${pk}>`
};

// layui table重载
export const layTableReload = (tableID, query=null) => {
    if (tableID) {
        layui.table.reload(tableID, {
            where: query, //设定异步数据接口的额外参数
            page: {curr: 1,}
        });
    } else {
        layui.layer.msg('There is no table id')
    }
};

// layui table自定义工具栏图标
export const layTableToolBar = {
    add: {
        title: '新增', // 标题
        layEvent: 'TABLE_ADD', // 事件名，用于 toolbar 事件中使用
        icon: 'layui-icon-add-1', // 图标类名
    },
    delete: {
        title: '删除',
        layEvent: 'TABLE_DELETE',
        icon: 'layui-icon-delete',
    }
};

// 关闭当前层弹出的模态框
export const closeIframe = () => {
    const index = parent.layui.layer.getFrameIndex(window.name);
    parent.layui.layer.close(index);
};

// 表格行工具事件处理
export const tableRowEventHandle = (obj, url=null, detail_callback=null, edit_callback=null, delete_callback=tableRowDeleteEvent) => {
    switch (obj.event) {
        case params.rowDetailEvent:
            if (detail_callback) {
                detail_callback(obj);
            } else {
                layer.msg('触发详情事件...');
            }
            break;
        case params.rowEditEvent:
            if (edit_callback) {
                edit_callback(obj);
            } else {
                layer.msg('触发编辑事件...');
            }
            break;
        case params.rowDeleteEvent:
            if (delete_callback) {
                delete_callback(obj, url);
            } else {
                layer.msg('触发删除事件...');
            }
            break;
    }
};

// 表格头部工具栏事件-批量删除
export const tableBulkDelete = (obj, url) => {
    const tableID = obj.config.id;

    // 获取批量选中的数据
    const checkData = layui.table.checkStatus(tableID);
    if (checkData.data.length) {
        let checkIDs = checkData.data.map((d) => {
            return d.id
        });

        const deleteData = {
            deleted: checkIDs.join(',')
        };

        // 执行批量删除
        layer.confirm('确定删除?', {icon: 2, title: '删除确认'}, function (index) {
            const response = syncApiResolve(url, deleteData, 'delete');
            if (response.result === params.resSuccessTip) {
                parent.layui.table.reload(tableID);  // 重载表格
                parent.layui.layer.close(index);
            }
        });
    }
};

// 表格头部工具事件处理
export const tableToolbarEventHandle = (obj, add_callback=null, delete_callback=null) => {
    switch (obj.event) {
        case layTableToolBar.add.layEvent:
            if (add_callback) {
                add_callback(obj);
            } else {
                layer.msg('触发新增事件...');
            }
            break;
        case layTableToolBar.delete.layEvent:
            if (delete_callback) {
                delete_callback(obj);
            } else {
                layer.msg('触发删除事件...');
            }
            break;
    }
};

// 异步api接口调用封装(暂时不考虑权限问题)
export const asyncApiResolve = (url, data=null, method='get', s_callback=null, c_callback=null, e_callback=null) => {
    let config = Object.assign({}, apiConfig);
    config.url = url;
    config.method = method;

    if (data) {
        config.data = data;
    }

    if (s_callback) {
        config.s_callback = s_callback;
    }

    if (e_callback) {
        config.e_callback = e_callback;
    }

    if (c_callback) {
        config.c_callback = c_callback;
    }

    api(config);
};

// 同步api接口调用封装(暂时不考虑权限问题)
export const syncApiResolve = (url, data=null, method='get', s_callback=null, c_callback=null, e_callback=null) => {
    let config = Object.assign({}, apiConfig);
    config.url = url;
    config.method = method;
    config.async = false;

    if (data) {
        config.data = data;
    }

    if (s_callback) {
        config.s_callback = s_callback;
    }

    if (e_callback) {
        config.e_callback = e_callback;
    }

    if (c_callback) {
        config.c_callback = c_callback;
    }

    return api(config);
};

// 表格行删除事件
const tableRowDeleteEvent = (obj, url) => {
    layer.confirm('确定删除?', {icon: 2, title: '删除确认'}, function (index) {
        //向服务端发送删除指令
        const delete_url = `${url}/${obj.data.id}`;
        const response = syncApiResolve(delete_url, null, 'delete');

        if (response.result === params.resSuccessTip) {
            // 删除表格当前行并更新缓存
            obj.del();

            // 关闭当前提示框
            parent.layui.layer.close(index);
        }
    });
};


// 模态框-iframe
export const layerIframe = (url, title, iframeID, area, skin='layui-layer-lan') => {
    layui.layer.open({
        type: 2,
        title: title,
        id: iframeID,
        skin: skin,
        area: area,
        content: url,
        width: 1000,
    })
};

// 设置/获取指定对象的指定属性的值
export const assigmentAttribute = (obj, attribute, value=null) => {
    // 当value没有传值时，默认行为为获取属性值，传值了则为属性赋值
    if (value) {
        eval(`obj.${attribute} = value`);
    }

    return eval(`obj.${attribute}`)
};


// 表单赋值
export const formAssignment = (formFilter, data=null) => {
    if (data) {  // 传递了data时，直接怼指定表单进行赋值
        layui.form.val(formFilter, JSON.parse(JSON.stringify(data)));
    } else {  // 如果没传data，则从父页面的获取指定的data
        const parent_data = assigmentAttribute(parent.window, formFilter);
        if (parent_data) {  // 如果从父页面也没有获取到data，则终止程序
            formAssignment(formFilter, parent_data)
        }
    }
};


