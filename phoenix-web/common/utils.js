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

