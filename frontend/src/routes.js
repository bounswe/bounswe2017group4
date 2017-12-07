/* eslint no-unused-vars: 0 */  // --> OFF
import React from 'react';
import { Route, IndexRoute } from 'react-router';
import { BaseLayout, EdgeEdit, BookComments, NotFoundPage } from './views';

import requireAuth from './components/hoc/requireAuth';

export default (
    <Route>
        <Route path="/" component={BaseLayout}>
            <IndexRoute component={BookComments} title="Book Comments" />
            <Route path="edgeedit" component={requireAuth(EdgeEdit)} title="Edge Edit" />
        </Route>
        <Route path="*" component={BaseLayout}>
            <IndexRoute component={NotFoundPage} title="404" />
        </Route>
    </Route>
);