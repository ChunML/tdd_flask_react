import React from 'react';
import ReactDOM from 'react-dom';
import UsersList from './components/UsersList';

class App extends React.Component {
  constructor() {
    super();

    this.state = {
      users: []
    }
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

  render() {
    return (
      <section className='section'>
        <div className='container'>
          <div className='columns'>
            <div className='column is-one-third'>
              <br />
              <h1 className='title is-1'>All Users</h1>
              <hr />
              <UsersList
                users={this.state.users}
              />
            </div>
          </div>
        </div>
      </section>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
