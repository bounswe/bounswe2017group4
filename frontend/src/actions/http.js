import { beginAjaxCall, ajaxCallSuccess, ajaxCallError } from './ajaxStatus';
import * as httpService from '../services/httpService';

/**
* http get request
*/
export const get = (url, params, onSuccess, onError, showError, baseUrl, removeToken) => {
    return dispatch => {
        dispatch(beginAjaxCall());
        httpService.get(url, params, response => {
            dispatch(ajaxCallSuccess());
            onSuccess(response);
        }, response => {
            dispatch(ajaxCallError());
            if (onError) {
                onError(response);
            }
        },
            showError, baseUrl, removeToken);
    };
};

/**
* http post request
*/
export const post = (url, data, onSuccess, onError, showError, baseUrl, removeToken) => {
    return dispatch => {
        dispatch(beginAjaxCall());
        httpService.post(url, data, response => {
            dispatch(ajaxCallSuccess());
            onSuccess(response);
        }, response => {
            dispatch(ajaxCallError());
            if (onError) {
                onError(response);
            }
        },
            showError, baseUrl, removeToken);
    };
};

/**
* http put request
*/
export const put = (url, data, onSuccess, onError, showError, baseUrl, removeToken) => {
    return dispatch => {
        dispatch(beginAjaxCall());
        httpService.put(url, data, response => {
            dispatch(ajaxCallSuccess());
            onSuccess(response);
        }, response => {
            dispatch(ajaxCallError());
            if (onError) {
                onError(response);
            }
        },
            showError, baseUrl, removeToken);
    };
};

/**
* http delete request
*/
export const del = (url, data, onSuccess, onError, showError, baseUrl, removeToken) => {
    return dispatch => {
        dispatch(beginAjaxCall());
        httpService.del(url, data, response => {
            dispatch(ajaxCallSuccess());
            onSuccess(response);
        }, response => {
            dispatch(ajaxCallError());
            if (onError) {
                onError(response);
            }
        },
            showError, baseUrl, removeToken);
    };
};