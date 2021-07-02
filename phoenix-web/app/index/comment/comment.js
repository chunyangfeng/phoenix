import {asyncApiResolve, randomColor} from "../../../common/utils.js";
import {urls} from "../../../config/urls.js";
import {params} from "../../../config/params.js";

$(function () {
    const editor = editormd("commentEditor", {
        width: "90%",
        height: 240,
        path: "/phoenix-web/plugin/editormd/lib/",
        theme: "default",  // 主题设置
        previewTheme: "default",  // 主题设置
        editorTheme: "default",  // 主题设置
        markdown: "",
        codeFold: true,
        saveHTMLToTextarea: true,    // 保存 HTML 到 Textarea
        searchReplace: true,
        watch : false,                // 关闭实时预览
        // htmlDecode: "style,script,iframe|on*",            // 开启 HTML 标签解析，为了安全性，默认不开启
        previewCodeHighlight : false, // 关闭预览 HTML 的代码块高亮，默认开启
        emoji: true,
        taskList: true,
        tex: true,                   // 开启科学公式TeX语言支持，默认关闭
        autoFocus: false,       // 取消自动聚焦编辑器输入框
        placeholder: "欢迎留下神评~",
        toolbarIcons : function() {
            return [
                "undo", "redo", "|",
                "bold", "del", "italic", "quote", "uppercase", "lowercase", "|",
                "h1", "h2", "h3", "h4", "h5", "h6", "|",
                "list-ul", "list-ol", "hr", "|",
                "help", "info"
            ]
        },
    });
});

const initialCommentData = (page=1, limit=10) => {
    const successCallback = (response) => {
        let data = response.data;

        if (data.length === 0) {
            // layui.jquery('#commentCount').addClass('layui-hide').prev().addClass('layui-hide')
            // layui.jquery('#commentPagination').addClass('layui-hide')
        } else {
            layui.jquery('#commentCount div:first').empty().text(`评论总数 ${data.length}`)
        }

        const commentElem = layui.jquery('#commentList');
        commentElem.empty();

        layui.laypage.render({
            elem: 'commentPagination',
            count: response.count,
            limit: limit,
            curr: page,
            groups: limit,
            layout: ['prev', 'page', 'next', 'count', 'skip'],
            jump: (obj, first) => {
                if (!first) {
                    initialCommentData(obj.curr, obj.limit);
                }
            },
        });

        layui.jquery.each(data, (index, value) => {
            let childHtml = '';
            if (value.comment.length > 0) {
                childHtml += `<div class="article-body-comment-show-card-body-child">
                                    <div class="article-body-comment-show-card layui-row">
                                    <div class="article-body-comment-show-card-child-img layui-col-md3" 
                                    style="background-color: ${randomColor()};color: ${randomColor()}">
                                        <span>${value.comment[0].nickname[0].toUpperCase()}</span>
                                    </div>
                                    <div class="article-body-comment-show-card-body layui-col-md9">
                                        <div class="article-body-comment-show-card-body-nickname">${value.comment[0].nickname}</div>
                                        <div class="article-body-comment-show-card-body-comment">
                                            ${value.comment[0].html_content}
                                        </div>
                                        <div class="article-body-comment-show-card-body-ctime">${value.comment[0].ctime}</div>
                                    </div>
                                </div>
                            </div>`;
            }

            const html = `<hr><div class="article-body-comment-show-card layui-row">
                    <div class="article-body-comment-show-card-img layui-col-md3" 
                    style="background-color: ${randomColor()};color: ${randomColor()}">
                        <span>${value.nickname[0].toUpperCase()}</span>
                    </div>
                    <div class="article-body-comment-show-card-body layui-col-md9">
                        <div class="article-body-comment-show-card-body-nickname">${value.nickname}</div>
                        <div class="article-body-comment-show-card-body-comment">${value.html_content}</div>
                        <div class="article-body-comment-show-card-body-ctime">${value.ctime}</div>
                        ${childHtml}
                    </div>
                </div>`
            commentElem.append(html);
        });
    }

    let queryString = `page=${page}&limit=${limit}`
    asyncApiResolve(`${urls.commentListApi}?${queryString}`, null, 'get', successCallback);
}

const initialVisitorInfo = () => {
    let username = localStorage.getItem(params.visitorName);
    let email = localStorage.getItem(params.visitorEmail);

    layui.form.val('commentFormFilter', {
        nickname: username,
        email: email
    })
}

const submitComment = (data) => {
    const sCallback = (res) => {
        initialCommentData();
        layui.form.val('commentFormFilter', {
            content: ""
        });
        layui.layer.msg("留言已提交，鉴于网站安全，您的留言需要通过审核之后才能展示，感谢您的理解。");
    }
    let formData = data.field;
    formData.html_content = formData['commentEditor-html-code'];
    delete formData['commentEditor-html-code'];

    asyncApiResolve(`${urls.commentListApi}`, formData, 'post', sCallback)
}

layui.jquery(document).ready(function () {
    initialCommentData()

    initialVisitorInfo()

    layui.form.on('submit(commentSubmit)', function (data) {
        submitComment(data);
        return false
    });
})