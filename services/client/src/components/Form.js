import React from 'react';
import { Redirect } from 'react-router-dom';

class Form extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      formData: {
        username: '',
        email: '',
        password: ''
      }
    };

    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
  }

  componentDidMount() {
    this.clearForm();
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.formType !== nextProps.formType) {
      this.clearForm();
    }
  }

  clearForm() {
    this.setState({
      formData: {
        username: '',
        email: '',
        password: ''
      }
    });
  }

  handleFormChange(e) {
    const { name, value } = e.target;
    this.setState(prev => ({
      formData: {
        ...prev.formData,
        [name]: value
      }
    }));
  }

  handleUserFormSubmit(e) {
    e.preventDefault();
    const { formType, loginUser } = this.props;
    const data = {
      email: this.state.formData.email,
      password: this.state.formData.password
    };
    if (formType === 'Register') {
      data.username = this.state.formData.username;
    }
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType.toLowerCase()}`;
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
        this.clearForm();
        loginUser(res.auth_token);
      })
      .catch(err => console.log(err));
  }

  render() {
    const { username, email, password } = this.state.formData;
    const { isAuthenticated, formType } = this.props;
    if (isAuthenticated) {
      return <Redirect to='/' />;
    }

    return (
      <div>
        {formType === 'Login' &&
          <h1 className='title is-1'>Log In</h1>
        }
        {formType === 'Register' &&
          <h1 className='title is-1'>Register</h1>
        }
        <hr/><br/>
        <form onSubmit={e => this.handleUserFormSubmit(e)}>
          {formType === 'Register' &&
            <div className='field'>
              <input
                name='username'
                className='input is-medium'
                type='text'
                placeholder='Enter a username'
                required
                value={ username }
                onChange={ this.handleFormChange }
              />
            </div>
          }
          <div className='field'>
            <input
              name='email'
              className='input is-medium'
              type='email'
              placeholder='Enter an email address'
              required
              value={ email }
              onChange={ this.handleFormChange }
            />
          </div>
          <div className='field'>
            <input
              name='password'
              className='input is-medium'
              type='password'
              placeholder='Enter a password'
              required
              value={ password }
              onChange={ this.handleFormChange }
            />
          </div>
          <input
            type='submit'
            className='button is-primary is-medium is-fullwidth'
            value='Submit'
          />
        </form>
      </div>
    );
  }
}

export default Form;