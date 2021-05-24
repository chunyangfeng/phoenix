import {asyncApiResolve, randomColor} from "../../../common/utils.js";
import {urls} from "../../../config/urls.js";
import {params} from "../../../config/params.js";

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
                                        <div class="article-body-comment-show-card-body-comment">${value.comment[0].content}</div>
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
                        <div class="article-body-comment-show-card-body-comment">${value.content}</div>
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
        })
    }
    let formData = data.field;
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