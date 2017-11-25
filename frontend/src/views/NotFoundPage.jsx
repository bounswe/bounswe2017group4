import React, { Component } from 'react';
import { Link } from 'react-router';

class NotFoundPage extends Component {

    render() {
        return (
            <div className="content">
                <center>
                    <h1>404 - Sayfa Bulunamadı</h1>
                    <p>Üzgünüz, böyle bir sayfa yok</p>
                    <Link to="/">Anasayfa</Link>
                </center>
            </div>
        );
    }
}

export default NotFoundPage;