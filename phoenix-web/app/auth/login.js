/*
** Author: Fengchunyang
** Date: 2021/2/22 7:08
** Blog: http://www.fengchunyang.com
*/
import {api, apiConfig} from '../../common/api.js'
import {urls} from "../../config/urls.js"

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
        localStorage.removeItem('token')
    }
    localStorage.setItem('token', response.extra.token);

    parent.layui.layer.msg(response.data);
    const index = parent.layer.getFrameIndex(window.name);
    parent.layui.layer.close(index);
};

// 登录提交
export const loginSubmit = (data) => {
    let config = Object.assign({}, apiConfig);
    config.url = urls.loginModule;
    config.data = data;
    config.s_callback = loginSuccessCallback;
    config.method = 'post';
    api(config);
};
