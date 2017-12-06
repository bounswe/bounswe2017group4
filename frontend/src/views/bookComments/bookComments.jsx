import React, { Component } from "react";
import { Card, CardActions, CardHeader, CardMedia, CardTitle, CardText } from 'material-ui/Card';
import * as http from '../../actions/http';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

class BookComments extends Component {
    constructor (props) {
        super(props);
        this.state = {
            searchText: "",
            comments: []
        };

        this.onChange = this.onChange.bind(this);
        this.onClick = this.onClick.bind(this);
    }

    onChange(e) {
        this.setState({
            searchText: e.target.value
        });

        // this.props.actions.get()
    }
    
    onClick() {

    }

    render() {
        let { searchText, comments } = this.state;
        return (
            <div>
                <input type="text" value={searchText} onChange={this.onChange} />
                {
                    searchText != "" &&
                    <MuiThemeProvider>
                        <Card>
                            <CardHeader title="Book name" subtitle="Book id" />
                            {
                                // comments.map((comment, index) => (
                                    <div>
                                        <CardTitle title="Username" subtitle="date" />
                                        <CardText>
                                            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                            Donec mattis pretium massa. Aliquam erat volutpat. Nulla facilisi.
                                            Donec vulputate interdum sollicitudin. Nunc lacinia auctor quam sed pellentesque.
                                            Aliquam dui mauris, mattis quis lacus id, pellentesque lobortis odio.
                                        </CardText>
                                        {
                                            this.props.isAuthenticated &&
                                            <CardActions>
                                                <button onClick={this.onClick} className="btn btn-fill btn-primary" type="submit">Delete Comment</button>
                                            </CardActions>
                                        }
                                    </div>
                                // ))
                            }
                        </Card>
                    </MuiThemeProvider>
                }
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated
});

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(http, dispatch)
});

export default connect(mapStateToProps, mapDispatchToProps)(BookComments);