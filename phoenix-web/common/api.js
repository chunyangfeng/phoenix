/*
** Author: Fengchunyang
** Date: 2021/2/22 7:29
** Blog: http://www.fengchunyang.com
** Desc: 全局api接口调用
*/
import {permissions} from "../config/permission.js";
import {globals} from "../config/params.js";

// 请求失败回调
const error_callback = (request, status, error) => {
    layer.msg(request)
};

export const apiConfig = {
    url: '/',
    s_callback: undefined,
    b_callback: undefined,
    c_callback: undefined,
    e_callback: error_callback,
    method: 'get',
    data: {},
    dataType: 'json',
    async: true,
};

export const api = (config,  perm = permissions.BASE) => {
    // ajax响应的数据
    let data = undefined;

    // 执行ajax请求
    layui.jquery.ajax({
        url: globals.apiPrefix + config.url,
        type: config.method,
        async: config.async,
        headers: {
            AuthPermission: perm
        },
        dataType: config.dataType,
        data: config.data,
        beforeSend: function (request) {
            // 请求发送前的回调处理
            if (config.b_callback) {
                config.b_callback(request)
            }
        },
        success: function (response, status) {
            // 请求成功后的回调处理
            if (config.s_callback) {
                config.s_callback(response, status)
            }
            data = response
        },
        error: function (request, status, error) {
            // 请求失败后的回调处理
            if (config.e_callback) {
                config.e_callback(request, status, error)
            }
        },
        complete: function (request, status) {
            // 请求完成后的回调处理，无论请求是否成功
            if (config.c_callback) {
                config.c_callback(request, status)
            }
        },
    });

    // api函数返回响应数据，当且仅当async的值设置为false(即同步请求时)，返回的值才有意义
    if (!config.async) {
        return data
    }
};

