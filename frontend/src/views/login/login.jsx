import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as http from '../../actions/http';
import { toastr } from 'react-redux-toastr';
import { MainContainer } from '../../components';
import { Field, reduxForm } from 'redux-form';
import { createValidator, required } from '../../common/validation';

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

    }

    render() {
        const { handleSubmit, submitting } = this.props;
        return (
            <MainContainer>
                <form className="form-horizontal" onSubmit={handleSubmit(this.handleSubmit)}>
                    <div className="row">
                        <div className="col-md-12">
                            <div className="form-group">
                                <div className="col-md-12">
                                    <Field className="col-md-6" name="username" component="input" type="text" placeholder="Username"/>
                                </div>
                                <div className="col-md-12">
                                    <Field className="col-md-6" name="password" component="input" type="password" placeholder="Password"/>
                                </div>
                                <div className="col-md-6">
                                    <button className="col-md-6">Login</button>
                                </div>
                                
                            </div>
                        </div>
                    </div>
                </form>
            </MainContainer>
        );
    }
}

let form = reduxForm({
    form: 'loginForm',
    validate
});

export default form(Login);