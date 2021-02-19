/*
** Author: Fengchunyang
** Date: 2021/2/19 17:03
** Blog: http://www.fengchunyang.com
*/
import {api} from "/phoenix-web/config/api.js"

layui.use('element', function () {
    let element = layui.element,
        layer = layui.layer,
        $ = layui.jquery;

    // '管理'按钮绑定事件
    $("#login").click(function () {
        layer.open({
            type: 2,
            title: '登录',
            id: 'login_iframe',
            skin: 'layui-layer-molv',
            area: ['40rem', '30rem'],
            content: api.login_page,
            width: 1000,
        })
    })
});

