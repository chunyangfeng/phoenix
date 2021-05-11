/*
** Author: Fengchunyang
** Date: 2021/2/19 17:03
** Blog: http://www.fengchunyang.com
*/

// 获取博客文章数据
import {asyncApiResolve, generateArticleCard, syncApiResolve} from "/phoenix-web/common/utils.js";
import {urls} from "../../config/urls.js";
import {params} from "../../config/params.js";


const getBlogData = (page=1, limit=10) => {
    const successCallback = (response) => {
        let card = '';

        layui.jquery.each(response.data, (index, value) => {
            card += generateArticleCard(value);
        });

        layui.jquery(params.articleCardElem).empty().append(card);

        layui.laypage.render({
            elem: params.articlePageElem,
            count: response.count,
            limit: limit,
            curr: page,
            groups: limit,
            layout: ['prev', 'page', 'next', 'count', 'skip'],
            jump: (obj, first) => {
                if (!first) {
                    getBlogData(obj.curr, obj.limit);
                }
            },
        });
    };

    const queryString = `page=${page}&limit=${limit}`;

    asyncApiResolve(`${urls.indexArticleListApi}?${queryString}`, null, 'get', successCallback);
};

const getShowCardData = () => {
    const successCallback = (response) => {
        const data = response.data;

        if (data.length === 1) {
            layui.jquery(`#${params.showCardArticleCountElem}`).empty().append(data[0].article_count);
            layui.jquery(`#${params.showCardCommentCountElem}`).empty().append(data[0].comment_count);
            layui.jquery(`#${params.showCardFansCountElem}`).empty().append(data[0].fans_count);
            layui.jquery(`#${params.showCardClassifyCountElem}`).empty().append(data[0].classify_count);
            layui.jquery(`#${params.showCardAccessCountElem}`).empty().append(data[0].access_count);
        }
    };
    asyncApiResolve(`${urls.showCardInfoApi}`, null, 'get', successCallback);
};

const visitorLogin = (callback) => {
    const email = localStorage.getItem(params.visitorEmail);

    if (!email) {
        layui.layer.open({
            type: 2,
            title: '访客信息',
            id: 'visitorInfoIframe',
            skin: 'layui-layer-molv',
            area: ['30rem', '20rem'],
            content: urls.visitorInfoPage,
        });
    } else {
        callback();
    }
};

const messageEvent = () => {
    const callback = () => {
        layui.layer.prompt({
            formType: 2,
            title: '请畅所欲言',
            area: ['600px', '250px']
        }, function (value, index, elem) {
            const data = {};
            data.name = localStorage.getItem(params.visitorName);
            data.email = localStorage.getItem(params.visitorEmail);
            data.message = value;

            asyncApiResolve(urls.visitorMessageListApi, data, 'post');
            layui.layer.close(index);
        });
    };

    visitorLogin(callback);
};

const subscribeEvent = () => {
    const callback = () => {
        const name = localStorage.getItem(params.visitorName);
        const email = localStorage.getItem(params.visitorEmail);
        const data = {
            name: name,
            email: email
        };
        const response = syncApiResolve(urls.visitorSubscribeListApi, {email: email}, 'patch');

        if (!response.data.is_repeat) {
            asyncApiResolve(urls.visitorSubscribeListApi, data, 'post');
            layui.layer.msg(`${email} 订阅成功`)
        } else {
            layui.layer.msg(`${email} 已订阅过`)
        }
    };

    layer.confirm('订阅成功后，本站的新文章发布/活动等将会通过订阅邮箱发送即时通知，取消订阅可以通过本站发送的邮件进行操作。',
        {icon: 3, title: '订阅提示'}, function (index) {
        visitorLogin(callback);

        layer.close(index);
    });
};

const getHotArticle = () => {
    const successCallback = (response) => {
        const data = response.data;
        const hotArticleElem = layui.jquery('#hotArticleList');
        hotArticleElem.empty();

        layui.jquery.each(data, (index, value) => {
            const html = `<a class="hot-article-elem" href="${value.link}">
                              ${index + 1}.${value.title} 
                          </a><hr>`;
            hotArticleElem.append(html);
        });
    };
    asyncApiResolve(`${urls.hotArticleInfoApi}`, null, 'get', successCallback);
};

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 获取博客文章数据
    getBlogData();

    // 获取展示卡数据
    getShowCardData();

    // 获取热门文章数据
    getHotArticle();

    // 私信操作
    layui.jquery('#message').on('click', () => {
        messageEvent();
    });

    // 订阅操作
    layui.jquery('#subscribe').on('click', () => {
        subscribeEvent();
    });
});

