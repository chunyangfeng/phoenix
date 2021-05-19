import {syncApiResolve, asyncApiResolve} from "../../../common/utils.js";
import {urls} from "../../../config/urls.js";

// 初始化日历
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

const initialCarousel = () => {
    layui.carousel.render({
        elem: "#dashboard-access",
        width: '100%',
        autoplay: false,
        height: '350px',
        indicator: 'outside',
        trigger: 'hover',
        arrow: 'none',
    })
}

// 堆叠区域折线图
const stackAreaLineCharts = () => {
    const charts = echarts.init(document.getElementById("accessStackAreaCharts"))
    let response = syncApiResolve(urls.dashboardAccessCharts, 'get')

    let option = {
        title: {
            text: '访问记录',
            x: 'center',
            y: '10px',
            textAlign: 'center',
            textStyle: {
                fontSize: 15,
                fontWeight: 500,
                fontFamily: 'Microsoft YaHei',
            },
        },
        grid: {
            show: true,
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'line',
                label: {
                    backgroundColor: '#009688'
                }
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: response.data.map(obj => {return obj.date}),
            axisLine: {
                color: '#009688'
            }
        },
        yAxis: {
            type: 'value',
            axisLine: {
                show: true,
                lineStyle: {
                    color: '#009688'
                }
            }
        },
        series: {
            name: '访问总量',
            type: 'line',
            stack: '总量',
            areaStyle: {
                color: '#009688'
            },
            lineStyle: {
                color: '#009688'
            },
            data: response.data.map(obj => {return obj.count})
        },
    };
    charts.setOption(option)
}

// 页面加载完毕后的动态操作
layui.jquery(document).ready(() => {
    // 渲染日历  TODO 考虑将日历替换为收录数据，用echarts仪表盘进行展示
    initialCalendar();

    // 加载统计数据
    initialStatisticData();

    // 渲染轮播图
    initialCarousel();

    // 渲染访问记录堆叠区域折线图
    stackAreaLineCharts();
})