/*
** Author: Fengchunyang
** Date: 2021/2/19 17:03
** Blog: http://www.fengchunyang.com
*/

// 获取博客文章数据
import {asyncApiResolve, generateArticleCard} from "../../common/utils.js";
import {urls} from "../../config/urls.js";
import {params} from "../../config/params.js";


const getBlogData = (page=1, limit=5) => {
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
            limits: [limit, limit*2, limit*4, limit*8, limit*16],
            curr: page,
            groups: limit,
            jump: (obj, first) => {
                if (!first) {
                    getBlogData(obj.curr, obj.limit);
                }
            },
        });
    };

    const queryString = `page=${page}&limit=${limit}&is_publish=1`;

    asyncApiResolve(`${urls.articleListApi}?${queryString}`, null, 'get', successCallback);
};

// 页面加载时的动态操作
layui.jquery(document).ready(function () {
    // 获取博客文章数据
    getBlogData();
});

