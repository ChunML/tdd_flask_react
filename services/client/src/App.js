import React from 'react';
import { Switch, Route } from 'react-router-dom';
import UsersList from './components/UsersList';
import About from './components/About';
import Navbar from './components/Navbar';
import Form from './components/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';

export default class App extends React.Component {
  constructor() {
    super();

    this.state = {
      users: [],
      username: '',
      email: '',
      title: 'TrungTran',
      formData: {
        username: '',
        email: '',
        password: ''
      },
      isAuthenticated: false
    };

    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
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

  addUser(event) {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email
    };

    fetch(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(res => {
        this.getUsers();
        this.setState({
          username: '',
          email: ''
        })
      })
      .catch(err => console.log(err));
  }

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj)
  }

  handleUserFormSubmit(e) {
    e.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data = {
      email: this.state.formData.email,
      password: this.state.formData.password
    };
    if (formType === 'register') {
      data['username'] = this.state.formData.username;
    }
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`
    fetch(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(res => res.json())
      .then(res => {
        this.clearFormState();
        window.localStorage.setItem('authToken', res.auth_token);
        this.setState({ isAuthenticated: true });
        this.getUsers();
      })
      .catch(err => console.log(err))
  }

  clearFormState() {
    this.setState({
      formData: {username: '', email: '', password: ''},
      username: '',
      email: ''
    });
  }

  handleFormChange(e) {
    const { name, value } = e.target;
    this.setState(prevState => ({
      formData: {
        ...prevState.formData,
        [name]: value
      }
    }));
  }

  logoutUser() {
    window.localStorage.clear();
    this.setState({ isAuthenticated: false });
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
                      formData={this.state.formData}
                      handleUserFormSubmit={this.handleUserFormSubmit}
                      handleFormChange={this.handleFormChange}
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )} />
                  <Route exact path='/login' render={() => (
                    <Form
                      formType='Login'
                      formData={this.state.formData}
                      handleUserFormSubmit={this.handleUserFormSubmit}
                      handleFormChange={this.handleFormChange}
                      isAuthenticated={this.state.isAuthenticated}
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