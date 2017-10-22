/* eslint no-unused-vars: 0 */  // --> OFF
import React from 'react';
import { Route, IndexRoute } from 'react-router';
import { BaseLayout, HomePage, SubView, Login, NotFoundPage } from './views';

import requireAuth from './components/hoc/requireAuth';

export default (
    <Route>
        <Route path="/" component={BaseLayout}>
            <IndexRoute component={HomePage} title="Home" />
            <Route path="/subview" component={SubView} title="SubView" />
            <Route path="/login" component={Login} title="Login"/>
        </Route>
        <Route path="*" component={BaseLayout}>
            <IndexRoute component={NotFoundPage} title="404" />
        </Route>
    </Route>
);

/*
 <Route>
        <Route path="/" component={requireAuth(BaseLayout)}>
            <IndexRoute component={requireAuth(HomePage)} title="Anasayfa" />
            <Route path="/subview" component={requireAuth(SubView)} title="SubView" />
        </Route>        
        <Route path="*" component={requireAuth(BaseLayout)}>
            <IndexRoute components={requireAuth(NotFoundPage)} title="404" />
        </Route>
    </Route>
*/