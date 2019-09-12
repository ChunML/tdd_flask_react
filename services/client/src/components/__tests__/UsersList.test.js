import React from 'react';
import { shallow } from 'enzyme';
import UsersList from '../UsersList';
import renderer from 'react-test-renderer';

const users = [
  {
    'active': true,
    'email': 'chun@email.com',
    'username': 'chun',
    'id': 1
  },
  {
    'active': true,
    'email': 'tran@email.com',
    'username': 'tran',
    'id': 2
  }
]

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('chun');
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});