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
import ConfirmBox from '../../components/common/confirmBox';

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
            answerList: []
        };
        
        this.getData = this.getData.bind(this);
        this.addResponseModal = this.addResponseModal.bind(this);
        this.addEdgeModal = this.addEdgeModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.openModalAsEditEdge = this.openModalAsEditEdge.bind(this);
        this.openModalAsDeleteResponse = this.openModalAsDeleteResponse.bind(this);
        this.onDeleteConfirm = this.onDeleteConfirm.bind(this);
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

    addResponseModal() {
        this.setState({
            isModalOpen: true,
            modalTitle: "New Response"
        });
    }

    addEdgeModal() {
        this.setState({
            isModalOpen: true,
            modalTitle: "New Edge"
        })
    }

    closeModal() {
        this.setState({ isModalOpen: false });
        this.props.initialize(null);
    }

    onDeleteConfirm(id) {
        let model = {
            edge_id: id
        };
        this.props.actions.post(
            "/deleteEdge",
            model,
            () => {
                this.closeModal();
                // toastr.success("Edge has been editted");
            },
            (error) => {
                // toastr.error(error);
            },
            true
        );
    }

    handleSubmit(props) {
        let { modalTitle } = this.state;
        if (modalTitle == "New Edge") {
            let model = {
                current_state_id: props.current_state_id,
                user_response: props.user_response,
                next_state_id: props.next_state_id,
                recommended_response: props.recommended_response
            };
            this.props.actions.post(
                "/addEdge",
                model,
                () => {
                    // toastr.success("New edge is added");
                },
                error => {
                    // toastr.error(error);
                },
                true
            );
        }
        else if (modalTitle == "Edit Edge") {
            let model = {
                edge_id: props.id,
                current_state_id: props.current_state_id.current_state_id.id,
                user_response: props.user_response,
                next_state_id: props.next_state_id.next_state_id.id,
                recommended_response: props.recommended_response
            };
            
            this.props.actions.post(
                "/editEdge",
                model,
                () => {
                    this.closeModal();
                    // toastr.success("Edge has been editted");
                },
                (error) => {
                    // toastr.error(error);
                },
                true
            );
        }
        // else if (modalTitle == "Delete Edge") {
        //     let model = {
        //         edge_id: props.id
        //     };
        //     this.props.actions.post(
        //         "/deleteEdge",
        //         model,
        //         () => {
        //             this.closeModal();
        //             // toastr.success("Edge has been editted");
        //         },
        //         (error) => {
        //             // toastr.error(error);
        //         },
        //         true
        //     );
        // }
        else if (modalTitle == "New Response") {
            let query = {
                state_id: props.current_state_id,
                chatbot_response: props.chatbot_response
            };
            this.props.actions.post(
                "/addResponse",
                query,
                () => {
                    this.closeModal();
                    // toastr.success("New chatbot response is added");
                },
                (error) => {
                    // toastr.error(error);
                },
                true
            );
        }
        else if (modalTitle == "Delete Response") {
            let query = {
                response_id: props.response_id
            };
            this.props.actions.post(
                "/deleteResponse",
                query,
                () => {
                    this.closeModal();                    
                    // toastr.success("Answer is deleted");
                },
                (error) => {
                    // toastr.error(error);
                },
                true
            );
        }

        this.getData();
    }

    openModalAsEditEdge(row) {
        let { dispatch } = this.props;

        this.props.initialize(row);
        this.setState({
            isModalOpen: true,
            modalTitle: "Edit Edge"
        });

        dispatch(change("edgeForm", "current_state_id", row));
        dispatch(change("edgeForm", "user_response", row.user_response));
        dispatch(change("edgeForm", "next_state_id", row));
        dispatch(change("edgeForm", "recommended_response", row.recommended_response));
    }

    openModalAsDeleteResponse(row) {
        this.setState({
            isModalOpen: true,
            modalTitle: "Delete Response"
        });

        this.props.actions.get(
            "/getResponses",
            null,
            (response) => {
                this.setState({
                    answerList: response.filter(item => item.state.id == row.id)
                });
            },
            (error) => {
                // toastr.error(error);
            },
            false
        );
    }

    detailFormatter(cell, row) {
        return (
            <div>
                <a title="Edit Edge" className="btn btn-simple btn-warning btn-icon table-action edit" href="javascript:void(0)" onClick={() => this.openModalAsEditEdge(row)}><i className="icon-pencil-square-o">Edit Edge</i></a>
                <ConfirmBox
                    showCancelButton={true}
                    onConfirm={() => this.onDeleteConfirm(row.id)} body="Are you sure?"
                    confirmText="Delete" identifier={row.id}>
                    <a title="Delete Edge" className="btn btn-simple btn-default btn-icon table-action remove colorDanger"><i className="icon-trash">Delete Edge</i></a>
                </ConfirmBox>
                <a title="Delete Response" className="btn btn-simple btn-warning btn-icon table-action remove colorDanger" href="javascript:void(0)" onClick={() => this.openModalAsDeleteResponse(row)}><i className="icon-pencil-square-o">Delete Response</i></a>
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
        let { isModalOpen, edgeList, currentPage, modalTitle, answerList } = this.state;
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
                        <button disabled={submitting} onClick={this.addEdgeModal} className="btn btn-fill btn-primary" type="submit">
                            New Edge
                        </button>
                        <br/>
                        <br/>
                        <button disabled={submitting} onClick={this.addResponseModal} className="btn btn-fill btn-primary" type="submit">
                            New Response
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
                                    modalTitle == "New Edge" &&
                                    <ModalBody>
                                        <div className="form-group">
                                            <div className="col-md-12">
                                                <Field name="current_state_id" type="text" placeholder="Select State" component={dropdown} label="Current State" data={edgeList} valueField="id" textField={item => item.current_state_id.description} filter="contains" />
                                            </div>
                                            <div className="col-md-12 mt20">
                                                <Field name="user_response" type="text" component={input} label="Enter a new intent" />
                                            </div>
                                            <div className="col-md-12">
                                                <Field name="next_state_id" type="text" placeholder="Select State" component={dropdown} label="Next State" data={edgeList} valueField="id" textField={item => item.next_state_id.description} filter="contains" />
                                            </div>
                                            <div className="col-md-12 mt20">
                                                <Field name="recommended_response" type="text" component={input} label="Enter a new recommended answer" />
                                            </div>
                                        </div>
                                    </ModalBody>
                                }
                                {
                                    modalTitle == "Edit Edge" &&
                                    <ModalBody>
                                        <div className="form-group">
                                            <div className="col-md-12">
                                            <Field name="current_state_id" type="text" placeholder="Select State" component={dropdown} label="Current State" data={edgeList} valueField="id" textField={item => item.current_state_id.description} filter="contains" />                                            
                                            </div>
                                            <div className="col-md-12 mt20">
                                                <Field name="user_response" type="text" component={input} label="Enter a new intent" />
                                            </div>
                                            <div className="col-md-12">
                                                <Field name="next_state_id" type="text" placeholder="Select State" component={dropdown} label="Next State" data={edgeList} valueField="id" textField={item => item.next_state_id.description} filter="contains" />
                                            </div>
                                            <div className="col-md-12 mt20">
                                                <Field name="recommended_response" type="text" component={input} label="Enter a new recommended answer" />
                                            </div>
                                        </div>
                                    </ModalBody>
                                }
                                {
                                    modalTitle == "New Response" &&
                                    <ModalBody>
                                        <div className="form-group">
                                            <div className="col-md-12">
                                                <Field name="current_state_id" type="text" placeholder="Select State" component={dropdown} label="Current State" data={edgeList} valueField="id" textField={item => item.current_state_id.description} filter="contains" />
                                            </div>
                                            <div className="col-md-12 mt20">
                                                <Field name="chatbot_response" type="text" component={input} label="Enter a new answer" />
                                            </div>
                                        </div>
                                    </ModalBody>
                                }
                                {
                                    modalTitle == "Delete Response" &&
                                    <ModalBody>
                                        <div className="form-group">
                                            <div className="col-md-12">
                                                <Field name="response_id" type="text" placeholder="Select an answer to deleted" component={dropdown} label="Answer List" data={answerList} valueField="id" textField={item => item.chatbot_response} filter="contains" />
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
