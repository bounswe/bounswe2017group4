import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as http from '../../actions/http';
import { toastr } from 'react-redux-toastr';
import { MainContainer } from '../../components';

class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            githubUser: null
        };
    }
    componentWillMount() {
        
    }

    render() {
        return (
            <MainContainer isTable={Boolean(false)}>
                Hello Master!!!
            </MainContainer>
        );
    }
}

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(http, dispatch)
});

export default connect(null, mapDispatchToProps)(HomePage);
