import React from 'react';
import { Switch, Route } from 'react-router-dom';
import UsersList from './components/UsersList';
import AddUser from './components/AddUser';
import About from './components/About';

export default class App extends React.Component {
  constructor() {
    super();

    this.state = {
      users: [],
      username: '',
      email: ''
    }

    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
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

  render() {
    return (
      <section className='section'>
        <div className='container'>
          <div className='columns'>
            <div className='column is-half'>
              <br />
              <Switch>
                <Route exact path='/' render={() => (
                  <div>
                    <h1 className='title is-1'>All Users</h1>
                    <hr /><br />
                    <AddUser
                      addUser={this.addUser}
                      username={this.state.username}
                      email={this.state.email}
                      handleChange={this.handleChange}
                    />
                    <br /><br />
                    <UsersList
                      users={this.state.users}
                    />
                  </div>
                )} />
                <Route exact path='/about' component={About} />
              </Switch>
            </div>
          </div>
        </div>
      </section>
    );
  }
}