import React from 'react';
import { shallow, mount } from 'enzyme';
import { MemoryRouter as Router } from 'react-router-dom';
import App from '../../App';

beforeAll(() => {
  global.localStorage = {
    getItem: () => 'someToken'
  };
});

test('App renders without crashing', () => {
  const wrapper = shallow(<App/>);
})

test('App will call componentDidMount when mounted', () => {
  const onDidMount = jest.fn();
  App.prototype.componentDidMount = onDidMount;
  const wrapper = mount(<Router><App/></Router>);
  expect(onDidMount).toHaveBeenCalledTimes(1);
})