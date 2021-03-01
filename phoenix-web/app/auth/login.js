/*
** Author: Fengchunyang
** Date: 2021/2/22 7:08
** Blog: http://www.fengchunyang.com
*/
import {api, apiConfig} from '../../common/api.js'
import {urls} from "../../config/urls.js"
import {asyncApiResolve} from "../../common/utils.js";

// 获取RSA公钥
export const getPublicKey = () => {
    let config = Object.assign({}, apiConfig);
    config.url = urls.publicKey;
    config.async = false;
    const response = api(config);
    return response.public_key
};

// 登陆成功回调
const loginSuccessCallback = (response, status) => {
    // 缓存登录后的token
    const token = localStorage.getItem('token');
    if (token) {
        localStorage.clear();
    }
    localStorage.setItem('token', response.extra.token);
    localStorage.setItem('username', response.extra.username);

    parent.layui.layer.msg(response.data);
    const index = parent.layer.getFrameIndex(window.name);
    parent.layui.layer.close(index);
    // 登录成功后重定向至后台管理首页
    parent.window.location.href = urls.dashboardPage;
};

// 登录提交
export const loginSubmit = (data) => {
    asyncApiResolve(urls.loginModule, data, 'post', loginSuccessCallback);
};
