import React, { Component } from "react";
import { Card, CardActions, CardHeader, CardMedia, CardTitle, CardText } from 'material-ui/Card';
import * as http from '../../actions/http';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import ConfirmBox from '../../components/common/confirmBox';
import { toastr } from 'react-redux-toastr';

class BookComments extends Component {
    constructor (props) {
        super(props);
        this.state = {
            searchText: "",
            bookName: "",
            comments: [],
            rating: 0
        };

        this.onChange = this.onChange.bind(this);
        this.onSearchClick = this.onSearchClick.bind(this);
        this.onDeleteConfirm = this.onDeleteConfirm.bind(this);
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
                });
            },
            null,
            true
        );

        this.props.actions.get(
            "/getRatings",
            query,
            response => {
                this.setState({
                    rating: response.rating
                });
            }
        );
    }
    
    onDeleteConfirm(id) {
        let query = {
            comment_id: id
        };
        this.props.actions.get(
            "/deleteComment",
            query,
            () => {
                // toastr.succes("Comment is successfully deleted");
            },
            (error) => {
                // toastr.error(error);
            },
            true
        );

        this.onSearchClick();
    }

    render() {
        let { searchText, comments, bookName, rating } = this.state;
        return (
            <div className="col-md-6 col-md-offset-3 text-center mt20">
                <div>
                    <input type="text" className="form-control text-primary" placeholder="Enter a book name" value={searchText} onChange={this.onChange} autoFocus="true" />
                </div>
                <div>
                    <button onClick={this.onSearchClick} className="btn btn-sm btn-fill btn-success mt10" type="submit">Search</button>
                    {
                        searchText != "" && comments.length != 0 &&
                        <MuiThemeProvider>
                            <Card className="cardStyle">
                                <CardHeader title={bookName} className="cardHeaderStyle" />
                                {
                                    comments.map((comment, index) => (
                                        <div key={index} className="cardGroupStyle">
                                            <CardTitle className="cardTitleStyle" subtitle={comment.user.name} />
                                            <CardText className="cardTextStyle">
                                                {comment.comment}
                                            </CardText>
                                            {
                                                this.props.isAuthenticated &&
                                                <CardActions>
                                                    <ConfirmBox
                                                        showCancelButton={true}
                                                        onConfirm={() => this.onDeleteConfirm(comment.id)} body="Are you sure?"
                                                        confirmText="Delete" cancelText="Cancel" identifier={comment.id}>
                                                        <a title="Delete" className="btn btn-simple btn-default btn-icon table-action remove"><i className="icon-trash">Delete Comment</i></a>
                                                    </ConfirmBox>
                                                </CardActions>
                                            }
                                        </div>
                                    ))
                                }
                            </Card>
                        </MuiThemeProvider>
                    }
                </div>
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