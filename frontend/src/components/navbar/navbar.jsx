import React, { Component } from 'react';
import Helmet from 'react-helmet';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as auth from '../../actions/auth';
import { browserHistory } from 'react-router';
import { Modal, ModalHeader, ModalTitle, ModalClose, ModalBody, ModalFooter } from 'react-modal-bootstrap';
import { Field, reduxForm } from 'redux-form';
import { toastr } from 'react-redux-toastr';
import * as http from '../../actions/http';

class NavBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isModalOpen: false
        };

        this.onClick = this.onClick.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.toggleMobileSideBar = this.toggleMobileSideBar.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    onClick() {
        this.props.auth.deauthenticate();
        browserHistory.push("/");
    }

    openModal() {
        this.setState({
            isModalOpen: true
        });
    }

    closeModal() {
        this.setState({ isModalOpen: false });
        this.props.initialize(null);
    }

    toggleMobileSideBar() {
        this.props.sideBarActions.openMobileSideBar();
    }

    handleSubmit(props) {
        let query = {
            name: props.username,
            password: props.password
        };
        this.props.http.get(
            "/isAdmin",
            query,
            response => {
                if (response) {
                    this.props.auth.authenticate();
                    browserHistory.push("/edgeedit");
                    toastr.success("Login successful");
                    this.closeModal();
                }
                else {
                    toastr.error("Login failed");
                }
            },
            null,
            true
        );
    }

    render() {
        let { isModalOpen } = this.state;
        let { handleSubmit, submitting } = this.props;
        return (
            <nav className="navbar navbar-default chitchat-navbar uxrocket">
                <Helmet htmlAttributes={{ "class": this.props.sideBar.isMobileSideBarOpen ? "nav-open" : "" }} />
                <button type="button" onClick={this.toggleMobileSideBar} className="navbar-toggle mobile-hamburger--open">
                    <span className="fa fa-bars"></span>
                </button>
                <div className="chitchat-navbar__logo"><a href="/"></a></div>
                <div className="chitchat-navbar__content">
                    <button type="button" className="navbar-toggle mobile-hamburger--open">
                        <span className="fa fa-hamburger-menu"></span>
                    </button>
                    {
                        !this.props.isAuthenticated &&
                        <ul className="nav navbar-nav chitchat-nav-right pull-right">
                            <li className="dropdown chitchat-nav-usermenu">
                                <div className="dropdown-toggle">
                                    <div className="chitchat-nav-usermenu-username">
                                        <button onClick={this.openModal} className="btn btn-fill btn-primary" type="submit">LOGIN</button>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    }
                    {
                        this.props.isAuthenticated &&
                        <ul className="nav navbar-nav chitchat-nav-right pull-right">
                            <li className="dropdown chitchat-nav-usermenu">
                                <div className="dropdown-toggle">
                                    <div className="chitchat-nav-usermenu-username">
                                        <span className="mr10">John Due</span>
                                        <button onClick={this.onClick} className="btn btn-fill btn-primary" type="submit">LOGOUT</button>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    }
                </div>
                <Modal isOpen={isModalOpen} onRequestHide={this.closeModal}>
                    <form className="form-horizontal" onSubmit={handleSubmit(this.handleSubmit)}>
                        <ModalHeader>
                            <ModalClose onClick={this.closeModal} />
                            <ModalTitle><div className="text-center text-primary">Login</div></ModalTitle>
                        </ModalHeader>
                        <ModalBody>
                            <div className="form-group">
                                <div className="col-md-6 col-md-offset-3">
                                    <Field className="col-md-12 form-control text-primary" name="username" component="input" type="text" placeholder="Username"/>
                                </div>
                                <div className="col-md-6 col-md-offset-3 mt10">
                                    <Field className="col-md-12 form-control text-primary" name="password" component="input" type="password" placeholder="Password"/>
                                </div>
                            </div>
                        </ModalBody>
                        <ModalFooter>
                            <div className="text-center">
                                <button className="btn btn-fill btn-tertiary" type="reset" onClick={this.closeModal}>
                                    Kapat
                                </button>
                                <button disabled={submitting} className="btn btn-fill btn-primary" type="submit">
                                Login
                            </button>
                            </div>
                        </ModalFooter>
                    </form>
                </Modal>
            </nav>
        );
    }
}

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated
});

const mapDispatchToProps = (dispatch) => ({
    auth: bindActionCreators(auth, dispatch),
    http: bindActionCreators(http, dispatch)
});

let form = reduxForm({
    form: "loginForm"
});

export default connect(mapStateToProps, mapDispatchToProps)(form(NavBar));