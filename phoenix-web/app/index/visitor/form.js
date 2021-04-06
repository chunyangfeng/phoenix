/*
** Author: Fengchunyang
** Date: 2021/4/6 11:00
** Blog: http://www.fengchunyang.com
*/

// 页面加载时的动态操作
import {params} from "/phoenix-web/config/params.js";

layui.jquery(document).ready(function () {
    // 访客登录
    layui.form.on('submit(visitorLoginFilter)', function (data) {
        localStorage.setItem(params.visitorName, data.field.name);
        localStorage.setItem(params.visitorEmail, data.field.email);

        const index = parent.layui.layer.getFrameIndex(window.name);
        parent.layui.layer.close(index);
    });
});