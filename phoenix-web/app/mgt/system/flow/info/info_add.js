/*
** Author: Fengchunyang
** Date: 2021/3/9 17:07
** Blog: http://www.fengchunyang.com
*/


import {params} from "../../../../../config/params.js";
import {asyncApiResolve, formAssignment, closeIframe, splitText} from "../../../../../common/utils.js";
import {urls} from "../../../../../config/urls.js";


// 项目信息 post成功后回调
const projectInfoSuccessCallback = (response) => {
    const status = response.responseJSON.result;
    if (status === params.resSuccessTip) {
        // 如果执行成功，则关闭当前iframe，同时刷新table
        closeIframe();
        parent.layui.table.reload(params.projectInfoTableID);
    }
};


// 页面加载后的动态操作
layui.jquery(document).ready(() => {
    // 编辑时表单赋值
    const projectInfoData = formAssignment(params.projectInfoFormFilter);

    //  项目日期范围选择器
    layui.laydate.render({
        elem: '#projectInfoStartDate',
        type: 'date',
        trigger: 'click',
    });
    layui.laydate.render({
        elem: '#projectInfoEndDate',
        type: 'date',
        trigger: 'click',
    });

    // 监听项目信息提交事件
    layui.form.on(`submit(${params.projectInfoFormSubmit})`, function (data) {
        let postData = data.field;
        // let date_range_arr = splitText(postData.date_range, params.dateRangeSeparator);
        //
        // postData.stime = date_range_arr[0];
        // postData.etime = date_range_arr[1];
        // delete postData['date_range'];

        if (projectInfoData) {
            asyncApiResolve(`${urls.projectInfoInfoApi}/${projectInfoData.id}`, postData, 'put',
                null, projectInfoSuccessCallback);
        } else {
            asyncApiResolve(urls.projectInfoListApi, postData, 'post', null, projectInfoSuccessCallback);
        }

        return false
    });
});

