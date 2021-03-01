/*
** Author: Fengchunyang
** Date: 2021/2/23 18:04
** Blog: http://www.fengchunyang.com
*/
import {urls} from "../config/urls.js";
import {api, apiConfig} from "../common/api.js";
import {permissions} from "../config/permission.js";
import {getRelativePath, dynamicClock, layTableReload, asyncApiResolve} from "../common/utils.js";


// 登出成功后的回调
const logoutSuccessCallback = (response, status) => {
    // 移除token
    localStorage.removeItem('token');
    // 重定向至首页
    window.location.href = urls.indexPage;
};

// 退出登录按钮绑定事件
layui.jquery('#logout').click(function () {
    asyncApiResolve(urls.logoutModule, null, 'get', logoutSuccessCallback)
});

// logo点击跳转
layui.jquery('#management-logo').click(function () {
    window.location.href = urls.indexPage;
});

// 初始化导航选中状态与展开状态
const initialNavStatus = () => {
    const url = getRelativePath();
    let pattern = new RegExp(url);
    layui.jquery(document.body).find('a').each(function (i, obj) {
        let str = layui.jquery(obj).attr('href');
        if (pattern.test(str)) {
            layui.jquery(obj).parent().addClass("layui-this");  // 高亮显示当前选中导航
            layui.jquery(obj).parent().parents().addClass("layui-nav-itemed");  // 展开上层导航
        }
    });
};

// 初始化登陆用户的信息
const initialUserInfo = () => {
    const username = localStorage.getItem('username');
    layui.jquery('#login-username').empty().append('<i class="layui-icon layui-icon-username"></i> '+username);
};

// 初始化动态时钟
const initialClock = () => {
    dynamicClock('management-footer');

    // 设置定时器每隔1秒（1000毫秒），调用函数执行，刷新时钟显示
    setInterval(function () {
        dynamicClock("management-footer");
    }, 1000);
};

// 页面加载时执行初始化操作
layui.jquery(document).ready(function () {
    initialNavStatus();

    initialUserInfo();

    initialClock();

    // 当reset按钮被点击时，如果是表格的搜索表单，则重载表格
    layui.jquery(':reset').click(function () {
        const tableID = this.getAttribute('tableID');
        if (tableID) {
            layTableReload(tableID);
        }
    });
});

