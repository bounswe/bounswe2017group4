import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';
import { routerReducer } from 'react-router-redux';
import ajaxCallInProgress from './ajaxStatus';
import sideBar from './sideBar';
import { reducer as toastrReducer } from 'react-redux-toastr';

const rootReducer = combineReducers({
    form: formReducer,
    ajaxCallInProgress,
    toastr: toastrReducer,
    routing: routerReducer,
    sideBar
});
export default rootReducer;
