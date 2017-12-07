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
            bookName: "",
            comments: []
        };

        this.onChange = this.onChange.bind(this);
        this.onSearchClick = this.onSearchClick.bind(this);
        this.onClick = this.onClick.bind(this);
    }

    onChange(e) {
        this.setState({
            searchText: e.target.value
        });
    }

    onSearchClick() {
        let query = {
            book_id: this.state.searchText
        };
        this.props.actions.get(
            "/getComments",
            query,
            response => {
                this.setState({
                    comments: response,
                    bookName: this.state.searchText
                })
                console.log(response);
            },
            null,
            true
        );
    }
    
    onClick() {

    }

    render() {
        let { searchText, comments, bookName } = this.state;
        return (
            <div>
                <input type="text" value={searchText} onChange={this.onChange} />
                <button onClick={this.onSearchClick} className="btn btn-fill btn-primary" type="submit">Search</button>
                {
                    searchText != "" && comments.length != 0 &&
                    <MuiThemeProvider>
                        <Card>
                            <CardHeader title={bookName} />
                            {
                                comments.map((comment, index) => (
                                    <div key={index}>
                                        <CardTitle subtitle={comment.user.name} />
                                        <CardText>
                                            {comment.comment}
                                        </CardText>
                                        {
                                            this.props.isAuthenticated &&
                                            <CardActions>
                                                <button onClick={this.onClick} className="btn btn-fill btn-primary" type="submit">Delete Comment</button>
                                            </CardActions>
                                        }
                                    </div>
                                ))
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