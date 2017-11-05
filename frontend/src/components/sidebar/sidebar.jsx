import React, { Component } from 'react';
import SideLink from '../sidelink/sidelink';

class SideBar extends Component {
    constructor(props) {
        super(props);
        this.toggleMobileSideBar = this.toggleMobileSideBar.bind(this);
    }
    
    toggleMobileSideBar() {
        this.props.sideBarActions.openMobileSideBar();
    }
    render() {
        return (

            <div className="sidebar" data-active-color="danger">
                <div className="sidebar-wrapper">
                    <div className="chitchat-usermobile">
                        <div className="mobile-header mobile-show" >
                            <div className="photo">
                                <img className="mobile-logo" src={require("../../static/img/logo.png")} />
                                <button type="button" className="navbar-toggle mobile-hamburger" onClick={this.toggleMobileSideBar}>
                                    <span className="fa fa-bars"></span>
                                </button>
                            </div>
                        </div>
                    </div>
                    <ul className="nav">
                        <SideLink onClick={this.toggleMobileSideBar}{...this.props} to="/" label="Home" icon="home" />
                    </ul>
                </div>
            </div>

        );
    }
}

export default SideBar;