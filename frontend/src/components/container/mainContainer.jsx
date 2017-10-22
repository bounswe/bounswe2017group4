import React, { Component } from 'react';

class MainContainer extends Component {
    render() {
        const _props = this.props;
        return (
            <div className="content">
                <div className="container-fluid">
                    <div className="row">
                        <div className={_props.containerColumnClass ? _props.containerColumnClass : "col-lg-12 col-md-12 "}>
                            <div className={this.props.isNotCard ? '' : 'card' }>
                                {
                                    _props.title &&
                                    <div className="header">
                                        <h4 className="title">
                                            {_props.title}
                                        </h4>
                                    </div>
                                }
                                <div className="content">
                                    {
                                        _props.isTable
                                            ?
                                            <div className="bootstrap-table">
                                                <div className="fixed-table-container">
                                                    {
                                                        _props.children
                                                    }
                                                </div>
                                            </div>
                                            :
                                            _props.children
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {
                    _props.modals ? _props.modals : null
                }
            </div>
        );
    }
}

export default MainContainer;