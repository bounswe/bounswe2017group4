import * as types from '../actions/types';
import { createReducer } from '../common/utils';

const initialState = {
    isMobileSideBarOpen: false
};

export default createReducer(initialState, {
    [types.OPEN_MOBILE_SIDEBAR]: (state) => {
        return Object.assign({}, state, {
            isMobileSideBarOpen: !state.isMobileSideBarOpen
        });
    }
});