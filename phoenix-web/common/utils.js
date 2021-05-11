/*
** Author: Fengchunyang
** Date: 2021/2/23 10:45
** Blog: http://www.fengchunyang.com
*/

// 全局变量
import {params} from "../config/params.js";
import {api, apiConfig} from "./api.js";
import {urls} from "../config/urls.js";

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

// 获取当前日期
export const getCurrentDate = (ym='年', md='月', dh='日', seq=' ', hm=':', ms=':') => {
    let time = new Date();  // 获得当前时间
    let year = time.getFullYear();  // 获得年月日
    let month = time.getMonth() + 1;  // 获得年月日,time的month默认为0-11，即0为1月，11为12月
    let date = time.getDate();  // 获得年月日
    let hour = time.getHours();  // 获得小时、分钟、秒
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

    return `${year}${ym}${month}${md}${date}${dh}${seq}${hour}${hm}${minute}${ms}${second}`
};

// 设置动态时钟
export const dynamicClock = (elem_id) => {
    const datetime_str = getCurrentDate();
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
    },
    update: {
        title: '批量更新',
        layEvent: 'TABLE_UPDATE',
        icon: 'layui-icon-survey',
    },
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
export const tableToolbarEventHandle = (obj, add_callback=null, delete_callback=null, update_callback=null) => {
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
        case layTableToolBar.update.layEvent:
            if (update_callback) {
                update_callback(obj);
            } else {
                layer.msg('触发批量更新事件...');
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
    if (data) {  // 传递了data时，直接对指定表单进行赋值
        layui.form.val(formFilter, JSON.parse(JSON.stringify(data)));
    } else {  // 如果没传data，则从父页面的获取指定的data
        const parent_data = assigmentAttribute(parent.window, formFilter);
        data = parent_data;
        if (parent_data) {  // 如果从父页面也没有获取到data，则终止程序
            formAssignment(formFilter, data)
        }
    }
    //  刷新表格渲染
    layui.form.render();
    return data
};

// 动态获取表单下拉框select的值
export const getLaySelectItem = (url, elem, pk, key, defaults=null) => {
    // lay select success callback
    const laySelectSuccessCallback = (response) => {
        layui.jquery.each(response.data, (index, value) => {
            const pkValue = assigmentAttribute(value, pk);  // 获取响应数据的主键值，提交数据时使用
            const textValue = assigmentAttribute(value, key);  // 获取响应数据中的展示字段值
            if (pkValue === Number(defaults)) {
                layui.jquery(elem).append(`<option value=${pkValue} selected>${textValue}</option>`)
            } else {
                layui.jquery(elem).append(`<option value=${pkValue}>${textValue}</option>`)
            }
        });

        // 手动渲染form表单中的select组件
        layui.jquery(elem).trigger('change');
        layui.form.render('select');
    };

    asyncApiResolve(url, null, 'get', laySelectSuccessCallback);
};

// 动态获取表单复选框的值
export const getLayCheckboxItem = (url, elem, pk, key, name, defaults=null) => {
    const layCheckboxSuccessCallback = (response) => {
        layui.jquery.each(response.data, (index, value) => {
            const pkValue = assigmentAttribute(value, pk);  // 获取响应数据的主键值，提交数据时使用
            const textValue = assigmentAttribute(value, key);  // 获取响应数据中的展示字段值
            if (defaults && defaults.indexOf(pkValue) !== -1) {
                layui.jquery(elem).append(`<input type="checkbox" name=${name} value=${pkValue} title=${textValue} checked>`)
            } else {
                layui.jquery(elem).append(`<input type="checkbox" name=${name} value=${pkValue} title=${textValue}>`)
            }
        });

        // 手动渲染form表单中的checkbox组件
        layui.jquery(elem).trigger('change');
        layui.form.render('checkbox');
    };

    asyncApiResolve(url, null, 'get', layCheckboxSuccessCallback);
};

// 获取复选框选中的数据
export const getCheckboxCheckedData = () => {
    const checkedArray = [];
    layui.jquery('input[type=checkbox]:checked').each(function () {
        checkedArray.push(layui.jquery(this).val());
    });
    return checkedArray
};

// 获取当前页面的query-string,name是query-string中的参数名称
export const getQueryString = (name) => {
    const reg = new RegExp(`(^|&)${name}=([^&]*)(&|$)`, 'i');
    const result = window.location.search.substr(1).match(reg);
    if (result !== null) {
        return unescape(result[2]);
    }
    return null;
};

// 动态生成文章卡片html
export const generateArticleCard = (data) => {
    let tags = '';
    layui.jquery.each(data.tags, (index, value) => {
        tags += `<span class="layui-badge layui-bg-green">${value.name}</span>`;
    });

    let isTop = '';
    if (data.is_top) {
        isTop += '[置顶] '
    }

    return `<div class="article-card">
                    <a class="article-card-pane" href="${urls.articleDetailPage}/${data.id}">
                        <div class="article-card-pane-item">
                            <h2 class="article-card-title">${isTop}${data.title}</h2>
                        </div>
                        <hr class="layui-bg-gray">
                        <div class="article-card-pane-item">
                            <h6 class="article-card-sub-title">
                              <span><i class="layui-icon layui-icon-user"></i> 作者 ${data.creator_display}</span>
                              <span><i class="layui-icon layui-icon-release"></i> 发表于 ${data.ptime}</span>
                              <span><i class="layui-icon layui-icon-app"></i> 分类 ${data.classify}</span>
                              <span><i class="layui-icon layui-icon-read"></i> 阅读量 ${data.read_count}</span>
                              <span><i class="layui-icon layui-icon-chat"></i> 评论数 ${data.comment_count}</span>
                            </h6>
                        </div>
                        <div class="article-card-pane-item">
                            <p class="article-card-desc">${data.desc}</p>
                        </div>
                        <div class="article-card-pane-item">
                            ${tags}
                        </div>
                    </a>
                </div>`;
};

// 分隔字符串,separator为字符串分隔符
export const splitText = (text, separator=',') => {
    return text.split(separator);
};

export const randomColor = (type = 'hex') => {
    // 生成随机颜色

    let red = Math.floor(Math.random() * 256);
    let green = Math.floor(Math.random() * 256);
    let blue = Math.floor(Math.random() * 256);

    let colors = '#00FF00';

    switch (type) {
        case "hex":
            colors = '#' + red.toString(16) + green.toString(16) + blue.toString(16);
            break;
        case "rgb":
            colors = '(' + red + ',' + green + ',' + blue + ')';
            break;
    }

    return colors
};

export const hexToRgb = (color) => {
    color = color.toLowerCase();
    let reg = /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/;

    if (color && reg.test(color)) {
        if (color.length === 4) {
            let colorNew = "#";

            for (let i = 1; i < 4; i += 1) {
                colorNew += color.slice(i, i + 1).concat(color.slice(i, i + 1));
            }
            color = colorNew;
        }
        //处理六位的颜色值
        let colorChange = [];
        for (let i = 1; i < 7; i += 2) {
            colorChange.push(parseInt("0x" + color.slice(i, i + 2)));
        }
        return "(" + colorChange.join(",") + ")";
    }

    return color
};

export const gradualChangeColor = (color, level = 0.5, type = 'light') => {
    // 得到rgb颜色值为color的减淡颜色值，level为加深的程度，限0-1之间
    let newColor = 'rgb(';

    color = color.substring(1, color.length);  // 删除rgb颜色字符串的第一个'('
    color = color.substring(0, color.length - 1);  // 删除rgb颜色字符串的最后一个')'
    color = color.split(',');

    for (let i = 0; i < 3; i++) {
        let value = parseInt(color[i].replace(/\s*/g, ""));
        if (type === 'light') {
            newColor += Math.floor((255 - value) * level + value);
        } else if (type === 'dark') {
            newColor += Math.floor(color[i] * (1 - level));
        } else {
            return new Error("未知的颜色渐变类型！");
        }

        if (i < 2) {
            newColor += ',';
        }
    }

    newColor += ')';

    return newColor;
};

export const randomInt = (range = 10) => {
    // 生成随机数

    let number = Math.random() * range;

    return Math.floor(number)
};



