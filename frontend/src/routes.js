/* eslint no-unused-vars: 0 */  // --> OFF
import React from 'react';
import { Route, IndexRoute } from 'react-router';
import { BaseLayout, Home, EdgeEdit, BookComments, Login, NotFoundPage } from './views';

import requireAuth from './components/hoc/requireAuth';

export default (
    <Route>
        <Route path="/login" component={Login} title="Login"/>
        <Route path="/" component={requireAuth(BaseLayout)}>
            <IndexRoute component={requireAuth(Home)} title="Home" />
            <Route path="edgeedit" component={requireAuth(EdgeEdit)} title="Edge Edit" />
            <Route path="bookcomments" component={BookComments} title="Book Comments" />
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