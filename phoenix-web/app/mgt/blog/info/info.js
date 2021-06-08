/*
** Author: Fengchunyang
** Date: 2021/3/1 17:39
** Blog: http://www.fengchunyang.com
*/

import {
    getLaySelectItem, getLayCheckboxItem, getCheckboxCheckedData, asyncApiResolve, formAssignment, getQueryString,
    syncApiResolve, getCurrentDate,
} from "../../../../common/utils.js";
import {urls} from "../../../../config/urls.js";
import {params} from "../../../../config/params.js";


$(function () {
    const editor = editormd("editor", {
        width: "100%",
        height: 740,
        path: "/phoenix-web/plugin/editormd/lib/",
        theme: "default",  // 主题设置
        previewTheme: "default",  // 主题设置
        editorTheme: "default",  // 主题设置
        markdown: "",
        codeFold: true,
        // autoHeight : true,  // 自动高度，通过正文内容自动撑开高度
        //syncScrolling : false,
        saveHTMLToTextarea: true,    // 保存 HTML 到 Textarea
        searchReplace: true,
        //watch : false,                // 关闭实时预览
        htmlDecode: "style,script,iframe|on*",            // 开启 HTML 标签解析，为了安全性，默认不开启
        //toolbar  : false,             //关闭工具栏
        //previewCodeHighlight : false, // 关闭预览 HTML 的代码块高亮，默认开启
        emoji: true,
        taskList: true,
        tocm: true,         // Using [TOCM]
        tex: true,                   // 开启科学公式TeX语言支持，默认关闭
        flowChart: true,             // 开启流程图支持，默认关闭
        sequenceDiagram: true,       // 开启时序/序列图支持，默认关闭,
        //dialogLockScreen : false,   // 设置弹出层对话框不锁屏，全局通用，默认为true
        //dialogShowMask : false,     // 设置弹出层对话框显示透明遮罩层，全局通用，默认为true
        //dialogDraggable : false,    // 设置弹出层对话框不可拖动，全局通用，默认为true
        //dialogMaskOpacity : 0.4,    // 设置透明遮罩层的透明度，全局通用，默认值为0.1
        //dialogMaskBgColor : "#000", // 设置透明遮罩层的背景颜色，全局通用，默认为#fff
        imageUpload: true,
        imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        imageUploadURL: "/Center/RichTextUpload",
        onload: function () {
            //console.log('onload', this);
            //this.fullscreen();
            //this.unwatch();
            //this.watch().fullscreen();

            //this.setMarkdown("#PHP");
            //this.width("100%");
            //this.height(480);
            //this.resize("100%", 640);
        }
    });
});

// 编辑行为时，为表单赋初值
const editActionInitial = () => {
    let formData = {};
    let articleID = getQueryString('articleID');
    if (articleID) {
        const response = syncApiResolve(`${urls.articleInfoApi}/${articleID}`,);
        formData = response.data;
        formAssignment(params.articleFormFilter, formData);

        formData.tags_id = formData.tags.map(item => item.id);
    }
    return formData
};

// 文章提交事件
const articleCommitEvent = (postData, edit_data, multiSelect) => {
    // editor.md自动生成的html格式的文章内容，字段为editor-html-code，转换为后端使用的字段
    postData.html_content = postData['editor-html-code'];
    delete postData['editor-html-code'];

    // 手动获取复选框选中的数据
    delete postData.tags;
    postData.tags_id = multiSelect.getValue().map(obj => {
        return obj.value
    });

    // 发布时间字段,当且仅当不为编辑模式时设置
    let now = getCurrentDate('-', '-', '');
    if (postData.is_publish && Object.keys(edit_data).length === 0) {
        postData['ptime'] = now;
    }

    const commitSuccessCallback = (response) => {
        if (response.result === params.resSuccessTip) {
            window.location.href = urls.articleListPage;  // 创建成功后跳转至列表页
        }
    };
    // 如果formData不为{}，则当前为编辑页面，调用put接口进行更新，否则为新增
    if (Object.keys(edit_data).length > 0) {
        postData['etime'] = now;  // 当为编辑模式时，设置编辑时间

        asyncApiResolve(`${urls.articleInfoApi}/${edit_data.id}`, postData, 'put', commitSuccessCallback);
    } else {
        asyncApiResolve(urls.articleListApi, postData, 'post', commitSuccessCallback);
    }
};

const initialTags = () => {
    // 初始化标签多选选择下拉框
    const response = syncApiResolve(urls.tagListApi, null, 'get');
    let tagsSelect = xmSelect.render({
        el: "#tagCheckboxElem",
        language: "zn",
        filterable: true,
        theme: {
            color: '#8dc63f',
        },
        data: response.data.map(obj => {
            return {
                name: obj.name,
                value: obj.id,
            }
        })
    });
    return tagsSelect
}

// 页面加载后的动态操作
layui.jquery(document).ready(function () {
    // 如果为编辑行为，则为表单赋初值
    const formData = editActionInitial();

    // 动态加载博客系列数据
    getLaySelectItem(urls.serialListApi, params.serialSelectElem, 'id', 'name', formData.serial_id);

    // 动态加载博客分类数据
    getLaySelectItem(urls.classifyListApi, params.classifySelectElem, 'id', 'name', formData.classify_id);

    // 动态加载博客标签数据
    // getLayCheckboxItem(urls.tagListApi, params.tagCheckboxElem, 'id', 'name', 'tags', formData.tags_id);

    const tagsSelect = initialTags();

    // 监听文章提交事件
    layui.form.on(`submit(${params.articleFormSubmit})`, function (data) {
        articleCommitEvent(data.field, formData, tagsSelect);
        return false
    });
});

