import React from 'react';
import { Modal, ModalHeader, ModalTitle, ModalClose, ModalBody, ModalFooter } from 'react-modal-bootstrap';

class ConfirmBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isConfirmBoxOpen: false,
            disableButton: false
        };

        this.onButtonClick = this.onButtonClick.bind(this);
        this.onConfirmClose = this.onConfirmClose.bind(this);
        this.onConfirm = this.onConfirm.bind(this);
    }

    onButtonClick() {
        this.setState({
            isConfirmBoxOpen: true
        });
    }

    onConfirmClose() {
        this.setState({
            isConfirmBoxOpen: false
        });
    }

    onConfirm() {
        this.setState({ isConfirmBoxOpen: false });
        this.props.onConfirm(this.props.identifier);
    }

    render() {
        let cancelButton = this.props.showCancelButton ?
            (<div className={this.props.cancelBSStyle} onClick={this.onConfirmClose}><i className="icon-times"></i> {this.props.cancelText}</div>) : null;
        let modal = (
            <Modal className="confirm-box" isOpen={this.state.isConfirmBoxOpen} onRequestHide={this.onConfirmClose}>
                <ModalHeader>
                    <ModalClose onClick={this.onConfirmClose} />
                    <ModalTitle>{this.props.title}</ModalTitle>
                </ModalHeader>
                <ModalBody>
                    {this.props.body}
                </ModalBody>
                <ModalFooter>
                    {cancelButton}
                    <button disabled={this.state.disableButton} className={this.props.confirmBSStyle} onClick={this.onConfirm}> <i className="icon-check"></i> {this.props.confirmText}</button>
                </ModalFooter>
            </Modal>
        );
        let content;
        if (this.props.children) {
            let btn = React.Children.only(this.props.children);
            content = React.cloneElement(btn, {
                onClick: this.onButtonClick,
                style: this.props.style
            },
                btn.props.children
            );
        } else {
            content = (
                <button onClick={this.onButtonClick} style={this.props.confirmBSStyle}>
                    {this.props.buttonText}
                </button>
            );
        }
        return (
            <span>
                {modal}
                {content}
            </span>
        );
    }
}

export default ConfirmBox;