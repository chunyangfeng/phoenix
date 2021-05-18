

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

// 页面加载完毕后的动态操作
layui.jquery(document).ready(() => {
    // 渲染日历  TODO 考虑将日历替换为收录数据，用echarts仪表盘进行展示
    initialCalendar();
})