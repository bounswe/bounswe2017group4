import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Field, reduxForm } from 'redux-form';
import * as http from '../../actions/http';
import { toastr } from 'react-redux-toastr';
import { MainContainer } from '../../components';
import { input, dropdown } from '../../components/common/inputComponents';
import ConfirmBox from '../../components/common/confirmBox';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Modal, ModalHeader, ModalTitle, ModalClose, ModalBody, ModalFooter } from 'react-modal-bootstrap';

class EdgeEdit extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentPage: 0,
            isModalOpen: false,
            modalTitle: "Yeni Kayıt",
            edgeList: []
        };
        
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.onDeleteConfirm = this.onDeleteConfirm.bind(this);
        this.openModalWithRow = this.openModalWithRow.bind(this);
        this.detailFormatter = this.detailFormatter.bind(this);
    }

    componentWillMount() {
        this.props.actions.get(
            "/getEdges", null,
            response => {
                console.log(response);
            },
            error => {
                console.log(error);
            }, true);
    }

    onPageChange() {
        
    }

    openModal() {
        this.setState({
            isModalOpen: true,
            modalTitle: "Yeni Kayıt"
        });
    }

    closeModal() {
        this.setState({ isModalOpen: false });
        this.props.initialize(null);
    }

    handleSubmit(props) {
        //eğer doluysa update yoksa new
    }

    onDeleteConfirm(id) {
        this.props.actions.del(
            "getEdges", null,
            response => {
                console.log(response);
            }, null, true);
    }

    openModalWithRow(row) {
        this.props.initialize(row);
        this.setState({
            isModalOpen: true,
            modalTitle: "Düzenle"
        });
    }

    detailFormatter(cell, row) {
        return (
            <div>
                <a title="Düzenle" className="btn btn-simple btn-default btn-icon table-action edit" href="javascript:void(0)" onClick={() => this.openModalWithRow(row)}><i className="icon-pencil-square-o">Edit</i></a>
                <ConfirmBox
                    showCancelButton={true}
                    onConfirm={() => this.onDeleteConfirm(row.id)} body="Silmek istediğinize emin misiniz?"
                    confirmText="Sil" cancelText="Vazgeç" identifier={row.id}>
                    <a title="Sil" className="btn btn-simple btn-default btn-icon table-action remove"><i className="icon-trash">Delete</i></a>
                </ConfirmBox>
            </div>
        );
    }

    render() {
        let { handleSubmit, submitting } = this.props;
        let { isModalOpen, edgeList, currentPage } = this.state;
        this.tableOptions = {
            page: currentPage,  // which page you want to show as default
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
                    fetchInfo={{ dataTotalSize: 10 }}
                    remote={true}
                    pagination={false}
                >
                    <TableHeaderColumn dataAlign="left" dataField="node_id" type="text" >Current Node</TableHeaderColumn>
                    <TableHeaderColumn dataAlign="left" dataField="response" type="text" >Response</TableHeaderColumn>
                    <TableHeaderColumn dataAlign="left" dataField="next_node" type="text" >Next Node</TableHeaderColumn>
                    <TableHeaderColumn dataAlign="right" dataField="id" type="text" columnClassName="td-actions text-right" dataFormat={this.detailFormatter} isKey={true} >&nbsp; </TableHeaderColumn>
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
                                    <Field name="state" placeholder="Birim seçiniz" type="text" component={dropdown} label="State seçiniz" data={edgeList} valueField="id" textField="description" filter="contains" />
                                </div>
                                <div className="col-md-12">
                                    <Field name="response" type="text" component={input} label="Cevabı seçiniz" />
                                </div>
                                <div className="col-md-12">
                                    <Field name="next_state" placeholder="Birim seçiniz" type="text" component={dropdown} label="Bir sonraki olması gereken statei seçiniz" data={edgeList} valueField="id" textField="description" filter="contains" />
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
