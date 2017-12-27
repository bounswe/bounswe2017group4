import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Field, reduxForm, change } from 'redux-form';
import * as http from '../../actions/http';
import { toastr } from 'react-redux-toastr';
import { MainContainer } from '../../components';
import { input, dropdown } from '../../components/common/inputComponents';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Modal, ModalHeader, ModalTitle, ModalClose, ModalBody, ModalFooter } from 'react-modal-bootstrap';

const defStyles = {
  open: {
    top: 100
  }
};

class EdgeEdit extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentPage: 0,
            isModalOpen: false,
            modalTitle: "",
            edgeList: [],
            modalType: 0,
            answerList: []
        };
        
        this.getData = this.getData.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.openModalAsEdit = this.openModalAsEdit.bind(this);
        this.openModalAsDelete = this.openModalAsDelete.bind(this);
        this.detailFormatter = this.detailFormatter.bind(this);
        this.stateDetailFormatter = this.stateDetailFormatter.bind(this);
    }

    componentWillMount() {
        this.getData();
    }

    getData() {
        this.props.actions.get(
            "/getEdges",
            null,
            response => {
                this.setState({
                    edgeList: response
                });
            },
            null,
            true
        );
    }

    openModal() {
        this.setState({
            isModalOpen: true,
            modalTitle: "New Edge",
            modalType: 0
        });
    }

    closeModal() {
        this.setState({ isModalOpen: false });
        this.props.initialize(null);
    }

    handleSubmit(props) {
        let { modalType } = this.state;
        if (modalType == 0) {
            console.log(props)
            let model = {
                state: props.state,
                chatbot_response: props.response
            };
            return this.props.actions.post(
                "/addResponse",
                model,
                () => {
                    toastr.success("New answer is added");
                },
                error => {
                    toastr.error(error);
                },
                true
            );
        }
        else if (modalType == 1) {
            let model = {
                current_state_id: props.current_state_id,
                user_response: props.user_response,
                next_state_id: props.next_state,
                recommended_response: props.recommended_response
            };
            this.props.actions.post(
                "/editEdge",
                model,
                () => {
                    toastr.success("Edge has been editted");
                },
                (error) => {
                    toastr.error(error);
                },
                true
            );
        }
        else if (modalType == 2) {
            let query = {
                response_id: props.answer
            };
            this.props.actions.get(
                "/deleteResponse",
                query,
                () => {
                    toastr.success("Answer is deleted");
                },
                (error) => {
                    toastr.error(error);
                },
                true
            );
        }

        this.getData();
    }

    openModalAsEdit(row) {
        let { dispatch } = this.props;
        console.log(row);

        this.props.initialize(row);
        this.setState({
            isModalOpen: true,
            modalTitle: "Edit Edge",
            modalType: 1
        });

        dispatch(change("edgeForm", "current_state", row.current_state_id.description));
        dispatch(change("edgeForm", "response", row.user_response));
        dispatch(change("edgeForm", "next_state", row));
    }

    openModalAsDelete(row) {
        this.props.actions.get(
            "/getResponses",
            null,
            response => {
                this.setState({
                    answerList: response.filter(item => item.state.id == row.current_state_id.id)
                });
            },
            null,
            true
        );
        console.log(row);

        this.setState({
            isModalOpen: true,
            modalTitle: "Delete answer",
            modalType: 2
        });
    }

    detailFormatter(cell, row) {
        return (
            <div>
                <a title="Edit" className="btn btn-simple btn-warning btn-icon table-action edit" href="javascript:void(0)" onClick={() => this.openModalAsEdit(row)}><i className="icon-pencil-square-o">Edit</i></a>
                <a title="Delete" className="btn btn-simple btn-warning btn-icon table-action remove colorDanger" href="javascript:void(0)" onClick={() => this.openModalAsDelete(row)}><i className="icon-pencil-square-o">Delete</i></a>
            </div>
        );
    }

    stateDetailFormatter(cell) {
        return (
            <div>
                {cell.description}
            </div>
        );
    }

    render() {
        let { handleSubmit, submitting } = this.props;
        let { isModalOpen, edgeList, currentPage, modalTitle, modalType, answerList } = this.state;
        this.tableOptions = {
            page: currentPage,  // which page you want to show as default
            sizePerPageList: [50, 100, 250], // you can change the dropdown list for size per page
            sizePerPage: 3,  // which size per page you want to locate as default
            pageStartIndex: 1, // where to start counting the pages
            paginationSize: 3,  // the pagination bar size.
            onSizePerPageList: this.onSizePerPageList,
            hideSizePerPage: true, // > You can hide the dropdown for sizePerPage
            noDataText: 'Veri Yok'
        };
        return (
            <MainContainer isTable={true}>
                <div className="panel bgNone">
                    <div className="panel-heading text-right">
                        <button disabled={submitting} onClick={this.openModal} className="btn btn-fill btn-primary" type="submit">
                            New Edge
                        </button>
                    </div>
                    <div className="panel-body">
                        <BootstrapTable
                            data={edgeList}
                            hover={true} bordered={false}
                            options={this.tableOptions}
                            fetchInfo={{ dataTotalSize: 10 }}
                            remote={true}
                            pagination={false}
                            striped
                        >
                            <TableHeaderColumn width="30%" dataAlign="left" dataField="current_state_id"  type="text" dataFormat={this.stateDetailFormatter}>
                                <span className="fontBold">Current State</span>
                            </TableHeaderColumn>
                            <TableHeaderColumn width="25%" dataAlign="left" dataField="user_response" type="text">
                                <span className="fontBold">Response</span>
                            </TableHeaderColumn>
                            <TableHeaderColumn width="30%" dataAlign="left" dataField="next_state_id" type="text" dataFormat={this.stateDetailFormatter}>
                                <span className="fontBold">Next State</span>
                            </TableHeaderColumn>
                            <TableHeaderColumn dataAlign="right" dataField="id" type="text" columnClassName="td-actions text-right" dataFormat={this.detailFormatter} isKey={true} ></TableHeaderColumn>
                        </BootstrapTable>
                        <Modal isOpen={isModalOpen} onRequestHide={this.closeModal} dialogStyles={defStyles}>
                            <form className="form-horizontal" onSubmit={handleSubmit(this.handleSubmit)}>
                                <ModalHeader>
                                    <ModalClose onClick={this.closeModal} />
                                    <ModalTitle>{modalTitle}</ModalTitle>
                                </ModalHeader>
                                {
                                    modalType == 0 &&
                                    <ModalBody>
                                        <div className="form-group">
                                            <div className="col-md-12">
                                                <Field name="state" type="text" placeholder="Select State" component={dropdown} label="Current State" data={edgeList} valueField="id" textField={item => item.current_state_id.description + " - " + item.user_response + " - " + item.next_state_id.description} filter="contains" />
                                            </div>
                                            <div className="col-md-12 mt20">
                                                <Field name="response" type="text" component={input} label="Enter a new answer" />
                                            </div>
                                        </div>
                                    </ModalBody>
                                }
                                {
                                    modalType == 1 &&
                                    <ModalBody>
                                        <div className="form-group">
                                            <div className="col-md-12">
                                            <Field disabled={true} name="current_state" type="text" component={input} label="Current State" />
                                            </div>
                                            <div className="col-md-12 mt20">
                                                <Field disabled={true} name="response" type="text" component={input} label="Response" />
                                            </div>
                                            <div className="col-md-12">
                                                <Field name="next_state" type="text" placeholder="Select State" component={dropdown} label="Next State" data={edgeList} valueField="id" textField={item => item.next_state_id.description} filter="contains" />
                                            </div>
                                        </div>
                                    </ModalBody>
                                }
                                {
                                    modalType == 2 &&
                                    <ModalBody>
                                        <div className="form-group">
                                            <div className="col-md-12">
                                                <Field name="answer" type="text" placeholder="Select an answer to delete" component={dropdown} label="Answer List" data={answerList} valueField="id" textField={item => item.chatbot_response} filter="contains" />
                                            </div>
                                        </div>
                                    </ModalBody>
                                }
                                <ModalFooter>
                                    <div className="text-center">
                                        <button className="btn btn-fill btn-tertiary" type="reset" onClick={this.closeModal}>
                                            Close
                                        </button>
                                        <button disabled={submitting} className="btn btn-fill btn-primary" type="submit">
                                            Submit
                                        </button>
                                    </div>
                                </ModalFooter>
                            </form>
                        </Modal>
                    </div>
                </div>
            </MainContainer>
        );
    }
}

let form = reduxForm({
    form: "edgeForm"
});

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(http, dispatch)
});

export default connect(null, mapDispatchToProps)(form(EdgeEdit));
