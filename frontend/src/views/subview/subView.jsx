import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as http from '../../actions/http';
import { toastr } from 'react-redux-toastr';
import { MainContainer } from '../../components';

class SubView extends Component {
    constructor(props) {
        super(props);
        this.state = {
            githubUser: null
        };
    }
    componentWillMount() {
        this.props.actions.get(
            'users/stanley', '',
            response => {
                toastr.success('Successfully connected Github API');
                this.setState({
                    githubUser: response
                });
            }, null, true);
    }

    render() {
        const _s = this.state;
        return (
            <MainContainer isTable={Boolean(false)}>

                {
                    _s.githubUser !== null
                    &&
                    <div className="row">
                        <div className="col-md-12">
                            <b>{'@' + _s.githubUser.login}</b>
                            <hr />
                            <ul className="github-user">
                                <li><img className="github-user-avatar" src={_s.githubUser.avatar_url} alt={_s.githubUser.name} /></li>
                                <li>{_s.githubUser.name} </li>
                                <li> {_s.githubUser.company} </li>
                                <li> {_s.githubUser.blog} </li>
                                <li> {_s.githubUser.location} </li>
                                <li> {_s.githubUser.email} </li>
                                <li>
                                    {_s.githubUser.created_at}
                                </li>
                            </ul>

                        </div>
                    </div>
                }
            </MainContainer>

        );
    }
}

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(http, dispatch)
});

export default connect(null, mapDispatchToProps)(SubView);
