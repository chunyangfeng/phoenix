/*
** Author: Fengchunyang
** Date: 2021/3/3 10:20
** Blog: http://www.fengchunyang.com
*/
import {asyncApiResolve, getRelativePath, randomColor} from "../../../common/utils.js";
import {urls} from "../../../config/urls.js";
import {params} from "../../../config/params.js";

$(function () {
    const editorDetail = editormd.markdownToHTML("editorDetail", {
        // htmlDecode: "style,script,iframe",
        // emoji: true,
        // taskList: true,
        // tocm: true,
        // tex: true, // 默认不解析
        // flowChart: true, // 默认不解析
        // sequenceDiagram: true, // 默认不解析
        // codeFold: true,
        // tocDropdown: true,
    });
});

const getArticleId = () => {
    let absPathArr = getRelativePath().split('/')
    return absPathArr[absPathArr.length - 1]
}

const initialCommentData = (reverse=false, page=1, limit=10) => {
    const successCallback = (response) => {
        let data = response.data;

        if (data.length === 0) {
            layui.jquery('#articleCommentCount').addClass('layui-hide').prev().addClass('layui-hide')
            layui.jquery('#articleCommentList').addClass('layui-hide').next().addClass('layui-hide')
            layui.jquery('#articleCommentPagination').addClass('layui-hide')
        }

        if (reverse) {
            data.reverse()
        }

        const articleCommentElem = layui.jquery('#articleCommentList');
        articleCommentElem.empty();

        layui.laypage.render({
            elem: 'articleCommentPagination',
            count: response.count,
            limit: limit,
            curr: page,
            groups: limit,
            layout: ['prev', 'page', 'next', 'count', 'skip'],
            jump: (obj, first) => {
                if (!first) {
                    console.log(obj)
                    initialCommentData(false, obj.curr, obj.limit);
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
            articleCommentElem.append(html);
        });
    }

    let articleId = getArticleId()
    let queryString = `page=${page}&limit=${limit}&article_id=${articleId}`
    asyncApiResolve(`${urls.articleCommentListApi}?${queryString}`, null, 'get', successCallback);
}

const initialVisitorInfo = () => {
    let username = localStorage.getItem(params.visitorName);
    let email = localStorage.getItem(params.visitorEmail);

    layui.form.val('articleCommentFormFilter', {
        nickname: username,
        email: email
    })
}

const submitComment = (data) => {
    const sCallback = (res) => {
        initialCommentData();
        layui.form.val('articleCommentFormFilter', {
            content: ""
        })
    }
    let formData = data.field;
    formData.article_id = getArticleId();
    asyncApiResolve(`${urls.articleCommentListApi}`, formData, 'post', sCallback)
}

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 动态加载评论数据
    initialCommentData();

    // 初始化访客信息
    initialVisitorInfo();

    // 监听评论表单提交事件
    layui.form.on('submit(articleCommentSubmit)', function (data) {
        submitComment(data);
        return false
    });

    // 评论排序事件
    layui.jquery('.article-body-comment-count-sort a').on('click', function () {
        let ascElem = layui.jquery('#articleCommentSortAsc')
        let dscElem = layui.jquery('#articleCommentSortDesc')
        let selectElem = layui.jquery(this)
        ascElem.removeClass('article-body-comment-count-sort-active')
        dscElem.removeClass('article-body-comment-count-sort-active')
        selectElem.addClass('article-body-comment-count-sort-active')

        let reverse = false
        if (selectElem.text() === '按时间正序') {
            reverse = true
        }
        initialCommentData(reverse)
    })
});

