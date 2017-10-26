import Request from 'superagent';
import { browserHistory } from 'react-router';
import * as constants from '../common/constants';
import { toastr } from 'react-redux-toastr';

/**
* http get request
*/
export const get = (url, params, onSuccess, onError, showError, baseUrl, removeToken) => {
    let requestUrl = constants.BUSINESS_SERVICE + url;
    let bearerToken = null;
    if (baseUrl) {
        requestUrl = baseUrl + url;
    }
    removeToken = "sadasdasdasd";
    if (!removeToken) {
        bearerToken = 'Bearer ' + localStorage.getItem('token');
    }

    return Request.get(requestUrl)
        .type('application/json')
        .query(params)
        .set('Authorization', bearerToken)
        .then(response => {
            onSuccess(response.body);
        }
        , response => {
            if (response.status == 401) {
                // browserHistory.push('/auth/logout');
            }
            if (response.status == 404) {
                toastr.error(response.message);
            }
            else if (response.status == 500 || response.status == undefined) {
                toastr.error('Sunucuyla iletişim kurulurken bir hata oluştu.');
            }
            else if (showError) {
                if (response.response && response.response.text) {
                    toastr.error(response.response.text);
                }
                else if (response.message) {
                    toastr.error(response.message);
                }
            }
            else {
                toastr.error(response.message);
            }
            onError(response);
        });
};

/**
* http post request
*/
export const post = (url, data, onSuccess, onError, showError, baseUrl, removeToken, isUrlEncoded = false) => {
    let requestUrl = constants.BUSINESS_SERVICE + url;
    let bearerToken = null;
    if (baseUrl) {
        requestUrl = baseUrl + url;
    }
    if (!removeToken) {
        bearerToken = 'Bearer ' + localStorage.getItem('token');
    }
    return Request.post(requestUrl)
        .type(isUrlEncoded ? 'application/x-www-form-urlencoded' : 'application/json')
        .set('Authorization', bearerToken)
        .send(isUrlEncoded ? data : data)
        .then(response => {
            onSuccess(response.body);
        }
        , response => {
            if (response.status == 401) {
                browserHistory.push('/auth/logout');
            }
            else if (response.status == 500 || response.status == undefined) {
                toastr.error('Sunucuyla iletişim kurulurken bir hata oluştu.');
            }
            else if (showError) {
                if (response.response && response.response.text) {
                    toastr.error('', response.response.text);
                }
                else if (response.message) {
                    toastr.error(response.message);
                }
            }
            onError(response);
        });
};

/**
* http put request
*/
export const put = (url, data, onSuccess, onError, showError, baseUrl, removeToken) => {
    let requestUrl = constants.BUSINESS_SERVICE + url;
    let bearerToken = null;
    if (baseUrl) {
        requestUrl = baseUrl + url;
    }
    if (!removeToken) {
        bearerToken = 'Bearer ' + localStorage.getItem('token');
    }
    return Request.put(requestUrl)
        .type('application/json')
        .set('Authorization', bearerToken)
        .send(data)
        .then(response => {
            onSuccess(response.body);
        }
        , response => {
            if (response.status == 401) {
                browserHistory.push('/auth/logout');
            }
            else if (response.status == 500 || response.status == undefined) {
                toastr.error('Sunucuyla iletişim kurulurken bir hata oluştu.');
            }
            else if (showError) {
                if (response.response && response.response.text) {
                    toastr.error(response.response.text);
                }
                else if (response.message) {
                    toastr.error(response.message);
                }
            }
            onError(response);
        });
};


/**
* http delete request
*/
export const del = (url, data, onSuccess, onError, showError, baseUrl, removeToken) => {
    let requestUrl = constants.BUSINESS_SERVICE + url;
    let bearerToken = null;
    if (baseUrl) {
        requestUrl = baseUrl + url;
    }
    if (!removeToken) {
        bearerToken = 'Bearer ' + localStorage.getItem('token');
    }
    return Request.del(requestUrl)
        .type('application/json')
        .set('Authorization', bearerToken)
        .send(data)
        .then(response => {
            onSuccess(response.body);
        }
        , response => {
            if (response.status == 401) {
                browserHistory.push('/auth/logout');
            }
            else if (response.status == 500 || response.status == undefined) {
                toastr.error('Sunucuyla iletişim kurulurken bir hata oluştu.');
            }
            else if (showError) {
                if (response.response && response.response.text) {
                    toastr.error(response.response.text);
                }
                else if (response.message) {
                    toastr.error(response.message);
                }
            }
            onError(response);
        });
};
