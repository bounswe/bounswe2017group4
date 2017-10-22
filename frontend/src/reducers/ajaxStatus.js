import {createReducer} from '../common/utils';
import * as types from '../actions/types';

const initialState = 0;

export default createReducer(initialState, {
    [types.BEGIN_AJAX_CALL]: (state) => {     
        return state + 1;
    },
    [types.AJAX_CALL_ERROR]: (state) => {
        return state - 1;
    },
     [types.AJAX_CALL_SUCCESS]: (state) => {
        return state - 1;
    }
});
