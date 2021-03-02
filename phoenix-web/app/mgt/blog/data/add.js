/*
** Author: Fengchunyang
** Date: 2021/3/1 8:41
** Blog: http://www.fengchunyang.com
*/
import {urls} from "../../../../config/urls.js";
import {params} from "../../../../config/params.js";
import {closeIframe, asyncApiResolve, formAssignment} from "../../../../common/utils.js";


// 博客分类 post成功后回调
const classify_c_callback = (response) => {
    const status = response.responseJSON.result;
    if (status === params.resSuccessTip) {
        // 如果执行成功，则关闭当前iframe，同时刷新table
        closeIframe();
        parent.layui.table.reload(params.classifyTableID);
    }
};

// 博客标签 post成功后回调
const tag_c_callback = (response) => {
    const status = response.responseJSON.result;
    if (status === params.resSuccessTip) {
        // 如果执行成功，则关闭当前iframe，同时刷新table
        closeIframe();
        parent.layui.table.reload(params.tagTableID);
    }
};


// 页面加载后的动态操作
layui.jquery(document).ready(function () {
    // 编辑时表单赋值
    const classifyData = formAssignment(params.classifyFormFilter);

    // 编辑时表单赋值
    const tagData = formAssignment(params.tagFormFilter);

    // 监听博客分类提交事件
    layui.form.on(`submit(${params.classifyAddSubmit})`, function (data) {
        if (classifyData) {
            asyncApiResolve(`${urls.classifyInfoApi}/${classifyData.id}`, data.field, 'put', null, classify_c_callback);
        } else {
            asyncApiResolve(urls.classifyListApi, data.field, 'post', null, classify_c_callback);
        }

        return false
    });

    // 监听博客分类提交事件
    layui.form.on(`submit(${params.tagAddSubmit})`, function (data) {
        if (tagData) {
            asyncApiResolve(`${urls.tagInfoApi}/${tagData.id}`, data.field, 'put', null, tag_c_callback);
        } else {
            asyncApiResolve(urls.tagListApi, data.field, 'post', null, tag_c_callback);
        }

        return false
    });
});
