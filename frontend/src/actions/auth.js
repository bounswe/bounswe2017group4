import * as types from './types';

export function authenticate() {
    return {
        type: types.AUTH_USER
    };
}