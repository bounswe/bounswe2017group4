import React, { Component } from 'react';
import Helmet from 'react-helmet';
import { HOME_LOGOUT } from '../../common/constants';

class NavBar extends Component {
    constructor(props) {
        super(props);
        this.toggleMobileSideBar = this.toggleMobileSideBar.bind(this);
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
                    <a className="navbar-brand mobile-hide">Title</a>
                    <button type="button" className="navbar-toggle mobile-hamburger--open">
                        <span className="fa fa-hamburger-menu"></span>
                    </button>
                    <ul className="nav navbar-nav chitchat-nav-right pull-right">
                        <li className="dropdown chitchat-nav-usermenu">
                            <div className="dropdown-toggle">
                                <div className="chitchat-nav-usermenu-username">
                                    John Due
                                    &nbsp;|&nbsp;
                                    <a href={HOME_LOGOUT}>ÇIKIŞ</a>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </nav>
        );
    }
}

export default NavBar;