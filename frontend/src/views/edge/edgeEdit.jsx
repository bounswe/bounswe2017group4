import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Field, reduxForm } from 'redux-form';
import * as http from '../../actions/http';
import { toastr } from 'react-redux-toastr';
import { MainContainer } from '../../components';
import { input, dropdown } from '../../components/common/inputComponents';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Modal, ModalHeader, ModalTitle, ModalClose, ModalBody, ModalFooter } from 'react-modal-bootstrap';

class EdgeEdit extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isModalOpen: false
        };
        
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    openModal() {
        this.setState({ isModalOpen: true });
    }

    closeModal() {
        this.setState({ isModalOpen: false });
        this.props.initialize(null);
    }

    handleSubmit(props) {

    }

    render() {
        let { handleSubmit, submitting } = this.props;
        let { isModalOpen } = this.state;
        this.tableOptions = {
            page: 0,  // which page you want to show as default
            sizePerPageList: [50, 100, 250], // you can change the dropdown list for size per page
            sizePerPage: 3,  // which size per page you want to locate as default
            pageStartIndex: 1, // where to start counting the pages
            paginationSize: 3,  // the pagination bar size.
            onSizePerPageList: this.onSizePerPageList,
            hideSizePerPage: true, // > You can hide the dropdown for sizePerPage
            noDataText: 'Veri Yok',
            onPageChange: this.onPageChange,
            onSortChange: this.onSortChange
        };
        return (
            <MainContainer isTable={true}>
                <button disabled={submitting} onClick={this.openModal} className="btn btn-fill btn-primary" type="submit">
                    Yeni Edge Ekle
                </button>
                <BootstrapTable
                    data={[{id: 0, node_id: 2, response: "hello", next_node: "5"}]}
                    hover={true} bordered={false}
                    options={this.tableOptions}
                    fetchInfo={{ dataTotalSize: 3 }}
                    remote={true}
                    pagination={true}
                >
                    <TableHeaderColumn dataAlign="center" dataField="node_id" type="text" >Current Node</TableHeaderColumn>
                    <TableHeaderColumn dataAlign="center" dataField="response" type="text" >Response</TableHeaderColumn>
                    <TableHeaderColumn dataAlign="center" dataField="next_node" type="text" >Next Node</TableHeaderColumn>
                    <TableHeaderColumn dataAlign="center" dataField="id" type="text" hidden={true} isKey={true} />
                </BootstrapTable>
                <Modal isOpen={isModalOpen} onRequestHide={this.closeModal}>
                    <form className="form-horizontal" onSubmit={handleSubmit(this.handleSubmit)}>
                        <ModalHeader>
                            <ModalClose onClick={this.closeModal} />
                            <ModalTitle>Edge Ekle</ModalTitle>
                        </ModalHeader>
                        <ModalBody>
                            <div className="form-group">
                                <div className="col-md-12">
                                    <Field name="state" type="text" component={dropdown} label="State seçiniz" />
                                </div>
                                <div className="col-md-12">
                                    <Field name="response" type="text" component={input} label="Cevabı seçiniz" />
                                </div>
                                <div className="col-md-12">
                                    <Field name="next_state" type="text" component={dropdown} label="Bir sonraki olması gereken statei seçiniz" />
                                </div>
                            </div>
                        </ModalBody>
                        <ModalFooter>
                            <button className="btn btn-fill btn-tertiary" type="reset" onClick={this.closeModal}>
                                Kapat
                            </button>
                            <button disabled={submitting} className="btn btn-fill btn-primary" type="submit">
                                Kaydet
                            </button>
                        </ModalFooter>
                    </form>
                </Modal>
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
