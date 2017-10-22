import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { browserHistory } from 'react-router';

export default function (ComposedComponent) {
    class Authentication extends Component {
        componentWillMount() {
            if (!this.props.isAuthenticated) {
                browserHistory.push('/auth/login');
            }
        }

        componentWillUpdate(nextProps) {
            if (!nextProps.isAuthenticated) {
                browserHistory.push('/auth/login');
            }
        }

        render() {
            return <ComposedComponent {...this.props} />;
        }
    }

    Authentication.propTypes = { isAuthenticated: PropTypes.bool };

    function mapStateToProps(state) {
        return { isAuthenticated: state.auth.isAuthenticated };
    }

    return connect(mapStateToProps)(Authentication);
}
