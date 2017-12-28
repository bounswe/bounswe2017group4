/*eslint-disable import/default */

import React from 'react';
import { render } from 'react-dom';
import configureStore from './store/configureStore';
import { Provider } from 'react-redux';
import { Router, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import routes from './routes';
import ReduxToastr from 'react-redux-toastr';
import './static/styles/index.scss';


const store = configureStore();
export const history = syncHistoryWithStore(browserHistory, store);

render(
    <Provider store={store}>
        <main>
            {/* <ReduxToastr timeOut={4000} newestOnTop={Boolean(true)} position="top-right" /> */}
            <Router history={history} routes={routes} />
        </main>
    </Provider>
    , document.getElementById('app-root')
);
