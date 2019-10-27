import React from 'react';
import { Redirect } from 'react-router-dom';
import { registerFormRules, loginFormRules } from './form-rules.js';
import FormErrors from './FormErrors';

class Form extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      formData: {
        username: '',
        email: '',
        password: ''
      },
      registerFormRules: registerFormRules,
      loginFormRules: loginFormRules,
      valid: false
    };

    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
  }

  componentDidMount() {
    this.clearForm();
    this.validateForm();
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.formType !== nextProps.formType) {
      this.clearForm();
      this.validateForm();
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

  allTrue() {
    let formRules = loginFormRules;
    if (this.props.formType === 'Register') {
      formRules = registerFormRules;
    }
    for (const rule of formRules) {
      if (!rule.valid) return false;
    }
    return true;
  }

  resetRules() {
    const {registerFormRules, loginFormRules} = this.state;
    for (const rule of registerFormRules) {
      rule.valid = false;
    }

    for (const rule of loginFormRules) {
      rule.valid = false;
    }
    this.setState({registerFormRules, loginFormRules, valid: false});
  }

  validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }

  validateForm() {
    const self = this;

    const formData = this.state.formData;
    self.resetRules();

    if (self.props.formType === 'Register') {
      const formRules = self.state.registerFormRules;
      if (formData.username.length > 5) {
        formRules[0].valid = true;
      }
      if (formData.email.length > 5) {
        formRules[1].valid = true;
      }
      if (this.validateEmail(formData.email)) {
        formRules[2].valid = true;
      }
      if (formData.password.length > 8) {
        formRules[3].valid = true;
      }
      self.setState({registerFormRules: formRules});
      if (self.allTrue()) {
        self.setState({valid: true});
      }
    }
    if (self.props.formType === 'Login') {
      const formRules = this.state.loginFormRules;
      if (formData.email.length > 0) {
        formRules[0].valid = true;
      }
      if (formData.password.length > 0) {
        formRules[1].valid = true;
      }
      self.setState({loginFormRules: formRules});
      if (self.allTrue()) {
        self.setState({valid: true});
      }
    }
  }

  handleFormChange(e) {
    const { name, value } = e.target;
    this.setState(prev => ({
      formData: {
        ...prev.formData,
        [name]: value
      }
    }), () => this.validateForm());
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

    let formRules = this.state.loginFormRules;

    if (formType === 'Register') {
      formRules = this.state.registerFormRules;
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
        <FormErrors
          formType={ formType }
          formRules={ formRules }
        />
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
            disabled={!this.state.valid}
          />
        </form>
      </div>
    );
  }
}

export default Form;