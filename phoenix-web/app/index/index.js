/*
** Author: Fengchunyang
** Date: 2021/2/19 17:03
** Blog: http://www.fengchunyang.com
*/
import {urls} from "/phoenix-web/config/urls.js"

// 获取登录状态

layui.use('element', function () {

    // '管理'按钮绑定事件
    layui.jquery("#management").click(function () {
        layui.layer.open({
            type: 2,
            title: '登录',
            id: 'login_iframe',
            skin: 'layui-layer-molv',
            area: ['40rem', '30rem'],
            content: urls.loginPage,
            width: 1000,
        })
    })
});

