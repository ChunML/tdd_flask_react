import React from 'react';
import { Link } from 'react-router-dom';

export default class UserStatus extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      email: '',
      id: '',
      username: '',
      active: '',
      admin: ''
    };

    this.getUserStatus = this.getUserStatus.bind(this);
  }

  componentDidUpdate() {
    if (this.props.isAuthenticated) {
      this.getUserStatus();
    }
  }

  getUserStatus(e) {
    return fetch(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${window.localStorage.authToken}`
      }
    })
      .then(res => res.json())
      .then(res => {
        this.setState({
          email: res.data.email,
          id: res.data.id,
          username: res.data.username,
          active: String(res.data.active),
          admin: String(res.data.admin)
        });
      })
      .catch(err => console.log(err));
  }

  render() {
    if (!this.props.isAuthenticated) {
      return (
        <p>You must be logged in to view this. Click <Link to='/login'>here</Link> to log back in.</p>
      );
    }
    return (
      <div>
        <ul>
          <li><strong>User ID:</strong> {this.state.id}</li>
          <li><strong>Email:</strong> {this.state.email}</li>
          <li><strong>Username:</strong> {this.state.username}</li>
          <li><strong>Active:</strong> {this.state.active}</li>
          <li><strong>Admin:</strong> {this.state.admin}</li>
        </ul>
      </div>
    );
  }
}