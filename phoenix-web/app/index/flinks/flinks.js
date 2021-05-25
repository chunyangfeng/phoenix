import {asyncApiResolve} from "../../../common/utils.js";
import {urls} from "../../../config/urls.js";


layui.jquery(document).ready(function () {
    // 表单提交
    layui.form.on('submit(flinksFormSubmit)', function (data) {
        asyncApiResolve(urls.flinkListApi, data.field, 'post', (res)=>{
            layui.layer.msg('提交成功，请等待审核')
        })
        return false
    })
})