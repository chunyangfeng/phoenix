/*
** Author: Fengchunyang
** Date: 2021/2/19 17:03
** Blog: http://www.fengchunyang.com
*/

// 获取博客文章数据
import {asyncApiResolve, generateArticleCard} from "/phoenix-web/common/utils.js";
import {urls} from "../../config/urls.js";
import {params} from "../../config/params.js";


const getBlogData = (page=1, limit=5) => {
    const baseLimit = 5;
    const successCallback = (response) => {
        let card = '';

        layui.jquery.each(response.data, (index, value) => {
            card += generateArticleCard(value);
        });

        layui.jquery(params.articleCardElem).empty().append(card);

        layui.laypage.render({
            elem: params.articlePageElem,
            count: response.count,
            limit: baseLimit,
            limits: [baseLimit, baseLimit*2, baseLimit*4, baseLimit*8, baseLimit*16],
            curr: page,
            groups: baseLimit,
            layout: ['prev', 'page', 'next', 'limit', 'count', 'skip'],
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

const messageEvent = () => {
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
    }
};

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 获取博客文章数据
    getBlogData();

    // 获取展示卡数据
    getShowCardData();

    // 私信操作
    layui.jquery('#message').on('click', () => {
        messageEvent();
    })
});

