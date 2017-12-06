import React, { Component } from 'react';
import Helmet from 'react-helmet';
import { connect } from 'react-redux';
import { SideBar, NavBar } from '../../components';
import ReduxToastr from 'react-redux-toastr';
import { bindActionCreators } from 'redux';
import * as sideBarActions from '../../actions/sideBar';

class BaseLayout extends Component {
    render() {
        let title = '';
        try {
            let currentRoute = this.props.routes[this.props.routes.length - 1];
            title = currentRoute['title'];
        }
        catch (err) { return; }

        return (
            <div className="wrapper">
                <NavBar {...this.props} />
                <Helmet
                    htmlAttributes={{ "lang": "tr", "amp": undefined }}
                    title={`ChitChat ▹ ${title}`}
                    meta={[
                        { "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0", "name": "viewport" },
                        { "http-equiv": "X-UA-Compatible", "content": "IE=edge,chrome=1" }
                    ]}
                    link={[
                        { "rel": "apple-touch-icon", "sizes": "76x76", "href": "/favicon.ico" },
                        { "rel": "icon", "sizes": "96x96", "href": require('../../static/img/favicon.ico') },
                        { "rel": "stylesheet", "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" }
                    ]}
                />
                <div className="main-panel">
                    {this.props.children}
                </div>
                <SideBar {...this.props} />
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    sideBar: state.sideBar
});

const mapDispatchToProps = (dispatch) => ({
    sideBarActions: bindActionCreators(sideBarActions, dispatch)
});

export default connect(mapStateToProps, mapDispatchToProps)(BaseLayout);


