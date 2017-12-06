import React, { Component } from 'react';
import Helmet from 'react-helmet';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as auth from '../../actions/auth';
import { browserHistory } from 'react-router';

class NavBar extends Component {
    constructor(props) {
        super(props);

        this.onClick = this.onClick.bind(this);
        this.toggleMobileSideBar = this.toggleMobileSideBar.bind(this);
    }

    onClick() {
        this.props.actions.deauthenticate();
        browserHistory.push("/");

    }

    toggleMobileSideBar() {
        this.props.sideBarActions.openMobileSideBar();
    }

    render() {
        return (
            <nav className="navbar navbar-default chitchat-navbar uxrocket">
                <Helmet htmlAttributes={{ "class": this.props.sideBar.isMobileSideBarOpen ? "nav-open" : "" }} />
                <button type="button" onClick={this.toggleMobileSideBar} className="navbar-toggle mobile-hamburger--open">
                    <span className="fa fa-bars"></span>
                </button>
                <div className="chitchat-navbar__logo"><a href="/"></a></div>
                <div className="chitchat-navbar__content">
                    <a className="navbar-brand mobile-hide">Admin Panel</a>
                    <button type="button" className="navbar-toggle mobile-hamburger--open">
                        <span className="fa fa-hamburger-menu"></span>
                    </button>
                    {
                        this.props.isAuthenticated &&
                        <ul className="nav navbar-nav chitchat-nav-right pull-right">
                            <li className="dropdown chitchat-nav-usermenu">
                                <div className="dropdown-toggle">
                                    <div className="chitchat-nav-usermenu-username">
                                        John Due
                                        &nbsp;|&nbsp;
                                        <button onClick={this.onClick} className="btn btn-fill btn-primary" type="submit">LOGOUT</button>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    }
                </div>
            </nav>
        );
    }
}

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated
});

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(auth, dispatch)
});

export default connect(mapStateToProps, mapDispatchToProps)(NavBar);