/*
** Author: Fengchunyang
** Date: 2021/3/9 18:02
** Blog: http://www.fengchunyang.com
*/

import {params} from "../../../../../config/params.js";
import {
    asyncApiResolve, formAssignment, closeIframe, getCurrentDate, getLaySelectItem
} from "../../../../../common/utils.js";
import {urls} from "../../../../../config/urls.js";


// 项目任务 post成功后回调
const projectTaskSuccessCallback = (response) => {
    const status = response.responseJSON.result;
    if (status === params.resSuccessTip) {
        // 如果执行成功，则关闭当前iframe，同时刷新table
        closeIframe();
        parent.layui.table.reload(params.projectTaskTableID);
    }
};


// 页面加载后的动态操作
layui.jquery(document).ready(() => {
    // 编辑时表单赋值
    const projectTaskData = formAssignment(params.projectTaskFormFilter);

    // 动态加载项目信息数据
    let project_id = projectTaskData ? projectTaskData.project: null;
    getLaySelectItem(urls.projectInfoListApi, params.projectInfoSelectElem, 'id', 'name', project_id);

    // 监听项目任务提交事件
    layui.form.on(`submit(${params.projectTaskFormSubmit})`, function (data) {
        let postData = data.field;

        if (projectTaskData) {
            postData['dtime'] = getCurrentDate('-', '-', '');

            asyncApiResolve(`${urls.projectTaskInfoApi}/${projectTaskData.id}`, postData, 'put',
                null, projectTaskSuccessCallback);
        } else {
            asyncApiResolve(urls.projectTaskListApi, postData, 'post', null, projectTaskSuccessCallback);
        }

        return false
    });
});