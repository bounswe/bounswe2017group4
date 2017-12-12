import React, { Component } from "react";
import { Card, CardActions, CardHeader, CardMedia, CardTitle, CardText } from 'material-ui/Card';
import * as http from '../../actions/http';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import ConfirmBox from '../../components/common/confirmBox';

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
    }
    
    onDeleteConfirm() {

    }

    render() {
        let { searchText, comments, bookName } = this.state;
        return (
            <div className="col-md-6 col-md-offset-3 text-center mt20">
                <div>
                    <input type="text" className="form-control text-primary" placeholder="Enter a book name" value={searchText} onChange={this.onChange} autoFocus="true" />
                </div>
                <div>
                    <button onClick={this.onSearchClick} className="btn btn-sm btn-fill btn-primary mt10" type="submit">Search</button>
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
                                                    <ConfirmBox
                                                        showCancelButton={true}
                                                        onConfirm={() => this.onDeleteConfirm(comment.id)} body="Silmek istediğinize emin misiniz?"
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