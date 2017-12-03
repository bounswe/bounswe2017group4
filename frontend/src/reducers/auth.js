/* eslint no-unused-vars: 0 */  // --> OFF
import { createReducer } from '../common/utils';
import { AUTH_USER } from '../actions/types';

const initialState = {
    isAuthenticated: false
};

export default createReducer(initialState, {
    [AUTH_USER]: (state) => {
        return Object.assign({}, state, {
            'isAuthenticated': true
        });
    }
});