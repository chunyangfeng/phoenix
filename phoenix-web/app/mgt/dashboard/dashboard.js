

// 初始化日历
import {asyncApiResolve} from "../../../common/utils.js";
import {urls} from "../../../config/urls.js";

const initialCalendar = () => {
    layui.laydate.render({
        elem: "#calendar",
        value: new Date(),  // 填充初始值为当前日期
        position: "static",  // 静态显示
        showBottom: false,  // 关闭底部按钮
        calendar: true,  // 显示公历节日
    })
}

const initialStatisticData = () => {
    const successCallback = (res) => {
        layui.jquery("#dashboardArticleCount").empty().text(res.data[0].article_count)
        layui.jquery("#dashboardCommentCount").empty().text(res.data[0].comment_count)
        layui.jquery("#dashboardTagCount").empty().text(res.data[0].tags_count)
        layui.jquery("#dashboardAccessCount").empty().text(res.data[0].access_count)
        layui.jquery("#dashboardUnpublishArticleCount").empty().text(res.data[0].unpublish_count)
        layui.jquery("#dashboardFlinkCount").empty().text(res.data[0].flink_apply)
        layui.jquery("#dashboardFansCount").empty().text(res.data[0].fans_count)
    }
    asyncApiResolve(urls.dashboardStatistic, null, 'get', successCallback);
}

// 页面加载完毕后的动态操作
layui.jquery(document).ready(() => {
    // 渲染日历  TODO 考虑将日历替换为收录数据，用echarts仪表盘进行展示
    initialCalendar();

    // 加载统计数据
    initialStatisticData();
})