/*
** Author: Fengchunyang
** Date: 2021/2/23 18:04
** Blog: http://www.fengchunyang.com
*/
import {urls} from "../config/urls.js";
import {api, apiConfig} from "../common/api.js";
import {permissions} from "../config/permission.js";

// 登出成功后的回调

const logoutSuccessCallback = (response, status) => {
    // 移除token
    localStorage.removeItem('token');
    // 重定向至首页
    window.location.href = urls.indexPage;
};

// 请求登出接口
const logoutSubmit = () => {
    let config = Object.assign({}, apiConfig);

    config.url = urls.logoutModule;
    config.s_callback = logoutSuccessCallback;
    api(config, permissions.LOGOUT);
};

// 退出登录按钮绑定事件
layui.jquery('#logout').click(function () {
    logoutSubmit();
});

// logo点击跳转
layui.jquery('#management-logo').click(function () {
    window.location.href = urls.indexPage;
});

