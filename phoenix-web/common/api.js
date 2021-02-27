/*
** Author: Fengchunyang
** Date: 2021/2/22 7:29
** Blog: http://www.fengchunyang.com
** Desc: 全局api接口调用
*/
import {permissions} from "../config/permission.js";
import {globals} from "../config/params.js";
import {urls} from "../config/urls.js";

// 403未授权处理
const authForbidden = () => {
    layui.layer.msg("你没有权限访问这个页面")
};

// 401未认证处理
const noPermission = () => {
    localStorage.clear();
    layui.layer.msg("你还没有登录系统，无法访问这个页面");
};

// 400错误处理
const badRequest = (error, reason) => {
    layui.layer.msg(error+": "+reason)
};

// 默认请求失败回调
const error_callback = (request, status, error) => {
    if (request.status === 403) {
        authForbidden();
    } else if (request.status === 401) {
        noPermission();
    } else if (request.status === 400) {
        const response = request.responseJSON;
        badRequest(response.result, response.data);
    }
};

// 默认请求成功回调
const success_callback = (response, status) => {
    layui.layer.msg(`${response.result}: ${response.data}`)
};

export const apiConfig = {
    url: '/',
    s_callback: success_callback,
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

    // 获取当前登录的用户信息，获取失败则为空字符串
    const token = localStorage.getItem('token') || '';

    // 执行ajax请求
    const loadIndex = layui.layer.load(1);

    layui.jquery.ajax({
        url: globals.apiPrefix + config.url,
        type: config.method,
        async: config.async,
        headers: {
            AUTH_PERMISSION: perm,
            AUTH_TOKEN: token
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
            data = response;

            layui.layer.close(loadIndex);  // 无论执行是否成功，都会解开load
        },
        error: function (request, status, error) {
            // 请求失败后的回调处理
            if (config.e_callback) {
                config.e_callback(request, status, error)
            }

            layui.layer.close(loadIndex);  // 无论执行是否成功，都会解开load
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

