import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as http from '../../actions/http';
import { toastr } from 'react-redux-toastr';
import { MainContainer } from '../../components';
import { Field, reduxForm } from 'redux-form';
import { createValidator, required } from '../../common/validation';
import * as auth from '../../actions/auth';
import { browserHistory } from 'react-router';

const validate = createValidator({
    name: required
});

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            
        };
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(props) {
        debugger
        this.props.actions.authenticate();
        toastr.success("Başarıyla giriş yapıldı");
        browserHistory.push("/");
    }

    render() {
        const { handleSubmit, submitting } = this.props;
        return (
            <div className="col-md-3 login-form">
                <MainContainer>
                    <form className="form-horizontal" onSubmit={handleSubmit(this.handleSubmit)} style={{ position: 'relative', overflow: 'hidden', float: 'none !important' }}>
                        <div className="row">
                            <div className="col-md-12">
                                <div className="form-group">
                                    <div className="col-md-12">
                                        <Field className="col-md-12" name="username" component="input" type="text" placeholder="Username"/>
                                    </div>
                                    <div className="col-md-12">
                                        <Field className="col-md-12" name="password" component="input" type="password" placeholder="Password"/>
                                    </div>
                                    <div className="col-md-12">
                                        <button className="btn btn-fill">Login</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </MainContainer>
            </div>
        );
    }
}

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(auth, dispatch)
});

let form = reduxForm({
    form: 'loginForm',
    validate
});

export default connect(null, mapDispatchToProps)(form(Login));