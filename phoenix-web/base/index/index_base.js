/*
** Author: Fengchunyang
** Date: 2021/3/2 19:26
** Blog: http://www.fengchunyang.com
*/

import {urls} from "/phoenix-web/config/urls.js"


layui.use('element', function () {

    // '管理'按钮绑定事件
    layui.jquery("#management").click(function () {
        // 判断是否登录,如果没有登录则进行登录，如果已经登录则跳转至后台管理页面
        const token = localStorage.getItem('token');
        if (!token) {
            layui.layer.open({
                type: 2,
                title: '登录',
                id: 'loginIframe',
                skin: 'layui-layer-molv',
                area: ['40rem', '30rem'],
                content: urls.loginPage,
                width: 1000,
            })
        } else {
            window.location.href = urls.dashboardPage;
        }
    })
});