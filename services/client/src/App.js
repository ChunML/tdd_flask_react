import React from 'react';
import { Switch, Route } from 'react-router-dom';
import UsersList from './components/UsersList';
import About from './components/About';
import Navbar from './components/Navbar';
import Form from './components/forms/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';
import Message from './components/Message';

export default class App extends React.Component {
  constructor() {
    super();

    this.state = {
      users: [],
      title: 'TrungTran',
      isAuthenticated: false,
      messageType: null,
      messageName: null
    };

    this.loginUser = this.loginUser.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
    this.createMessage = this.createMessage.bind(this);
  }

  componentDidMount() {
    if (window.localStorage.getItem('authToken')) {
      this.setState({ isAuthenticated: true }, () => {
        this.getUsers();
      });
    }
    this.getUsers();
  }

  getUsers() {
    fetch(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => res.json())
      .then(res => this.setState({users: res.data}))
      .catch(err => console.log(err));
  }

  loginUser(token) {
    window.localStorage.setItem('authToken', token);
    this.setState({ isAuthenticated: true });
    this.getUsers();
    this.createMessage('Welcome!', 'success');
  }

  logoutUser() {
    window.localStorage.clear();
    this.setState({ isAuthenticated: false });
  }

  createMessage(messageName='sanity check', messageType='success') {
    this.setState({
      messageName,
      messageType
    });
  }

  render() {
    return (
      <div>
        <Navbar
          title={this.state.title}
          isAuthenticated={this.state.isAuthenticated}
        />
        <section className='section'>
          <div className='container'>
            {
              this.state.messageName && this.state.messageType && (
                <Message
                  messageName={this.state.messageName}
                  messageType={this.state.messageType}
                />
              )
            }
            <div className='columns'>
              <div className='column is-half'>
                <br />
                <Switch>
                  <Route exact path='/' render={() => (
                    <UsersList
                      users={this.state.users}
                    />
                  )} />
                  <Route exact path='/about' component={About} />
                  <Route exact path='/register' render={() => (
                    <Form
                      formType='Register'
                      isAuthenticated={this.state.isAuthenticated}
                      loginUser={this.loginUser}
                      createMessage={this.createMessage}
                    />
                  )} />
                  <Route exact path='/login' render={() => (
                    <Form
                      formType='Login'
                      isAuthenticated={this.state.isAuthenticated}
                      loginUser={this.loginUser}
                      createMessage={this.createMessage}
                    />
                  )} />
                  <Route exact path='/logout' render={() => (
                    <Logout
                      logoutUser={this.logoutUser}
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )}/>
                  <Route exact path='/status' render={() => (
                    <UserStatus
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )} />
                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}