/*
** Author: Fengchunyang
** Date: 2021/2/23 10:45
** Blog: http://www.fengchunyang.com
*/

// 全局变量
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

