import React, { Component } from 'react';
import { Link } from 'react-router';
import './sidelink.scss';

class SideLink extends Component {
    render() {
        return (
            <li className={`${this.props.to === this.props.location.pathname ? 'active' : ''} ${this.props.className ? this.props.className : ''}`}>
                <Link to={this.props.to} onClick={this.props.onClick}>
                    <i className={`fa fa-${this.props.icon}`}></i>
                    <p>
                        <span>{this.props.label}</span>
                    </p>
                </Link>
            </li>
        );
    }
}

export default SideLink;